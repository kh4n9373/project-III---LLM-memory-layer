"""
Topic Segmentation Script for Locomo Dataset

This script performs topic segmentation on dialogue data from the Locomo dataset.
It splits long dialogues into coherent semantic segments based on intent/topic shifts.
"""

import json
import os
from typing import List, Dict, Any, Optional
from openai import OpenAI
from tqdm import tqdm
import argparse
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with support for custom base URL
def get_openai_client() -> OpenAI:
    """Get OpenAI client with custom base URL support."""
    api_key = os.environ.get("OPENAI_API_KEY")
    base_url = os.environ.get("OPENAI_BASE_URL")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    if base_url:
        print(f"Using custom base URL: {base_url}")
        return OpenAI(api_key=api_key, base_url=base_url)
    else:
        print("Using default OpenAI API")
        return OpenAI(api_key=api_key)

client = get_openai_client()

SEGMENTATION_PROMPT = """You are an expert at analyzing conversations and identifying topic boundaries.

Your task is to split the dialogue into coherent segments. Each segment should cluster turns that serve the same intent/topic.

**Cut criteria (when to start a new segment):**
1. Intent shift: The goal of the conversation changes (e.g., discussing career → discussing family)
2. Entity/Topic shift: The main subject changes significantly
3. Temporal cue: Clear time change mentioned ("yesterday", "next week", etc.)
4. Resolution point: A task or topic is clearly concluded

**Important guidelines:**
- Avoid over-segmentation: Don't cut for fillers ("uhm", "ok", greetings)
- Keep names, dates, and numbers in summaries
- Summaries should be 2-3 sentences
- Each segment must have at least 2 turns
- Be conservative: prefer fewer, larger segments over many small ones

**Input format:**
You will receive a dialogue with turn numbers in the format:
[Turn X] Speaker: content

**Output format:**
Return a JSON array of segments. Each segment must have:
- segment_id: Unique identifier (e.g., "seg_1", "seg_2")
- title: Short descriptive title (max 8 words)
- summary: 2-3 sentence summary preserving names, dates, and key details
- key_entities: Array of important entities (people, places, dates, events)
- salient_facts: Array of key facts to remember
- turn_indices: Array of turn numbers in this segment (e.g., [1, 2, 3, 4])
- boundary_reason: Why this segment starts here (for segments after the first)

Example output:
```json
[
  {
    "segment_id": "seg_1",
    "title": "Thesis timeline planning",
    "summary": "User needs help planning thesis defense timeline. Final defense is December 20. They are behind on experiments and need to create a weekly plan with task breakdown.",
    "key_entities": ["thesis", "defense", "December 20", "experiments"],
    "salient_facts": ["defense_date=2025-12-20", "behind_on_experiments=true"],
    "turn_indices": [1, 2, 3, 4, 7],
    "boundary_reason": null
  },
  {
    "segment_id": "seg_2",
    "title": "Server OOM troubleshooting",
    "summary": "New topic about server crash. Server experienced out-of-memory error. GPU is 24GB with batch size of 64. Assistant suggests reducing batch size to 16 with gradient accumulation.",
    "key_entities": ["server", "OOM", "GPU", "24GB", "batch size"],
    "salient_facts": ["oom_error=true", "gpu_memory=24GB", "current_batch=64", "suggested_batch=16"],
    "turn_indices": [5, 6, 8, 9, 10],
    "boundary_reason": "Intent/entity shift from academic planning to infrastructure troubleshooting"
  }
]
```

Now segment the following dialogue. Return only the JSON array, no additional text.
"""


def format_dialogue_for_segmentation(messages: List[Dict[str, str]]) -> str:
    """Format messages into a numbered dialogue string."""
    formatted_lines = []
    for i, msg in enumerate(messages, 1):
        role = msg.get("role", "Unknown")
        content = msg.get("content", "")
        formatted_lines.append(f"[Turn {i}] {role}: {content}")
    
    return "\n".join(formatted_lines)


def segment_dialogue_with_llm(
    messages: List[Dict[str, str]], 
    model: str = "gpt-4o",
    temperature: float = 0.3
) -> List[Dict[str, Any]]:
    """
    Use LLM to segment a dialogue into coherent topics.
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        model: OpenAI model to use
        temperature: Temperature for generation
        
    Returns:
        List of segment dictionaries
    """
    dialogue_text = format_dialogue_for_segmentation(messages)
    prompt = f"{SEGMENTATION_PROMPT}\n\nDialogue:\n{dialogue_text}"
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert dialogue analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            response_format={"type": "json_object"}
        )
        
        result = response.choices[0].message.content
        
        # Parse the JSON response
        # Sometimes the model wraps the array in an object
        parsed = json.loads(result)
        if isinstance(parsed, dict):
            # Try to find the segments array
            if "segments" in parsed:
                segments = parsed["segments"]
            else:
                # Take the first list value
                for value in parsed.values():
                    if isinstance(value, list):
                        segments = value
                        break
                else:
                    segments = []
        else:
            segments = parsed
            
        return segments
        
    except Exception as e:
        print(f"Error during segmentation: {e}")
        # Return a default single segment if segmentation fails
        return [{
            "segment_id": "seg_1",
            "title": "Full conversation",
            "summary": "Unable to segment - using full conversation as single segment.",
            "key_entities": [],
            "salient_facts": [],
            "turn_indices": list(range(1, len(messages) + 1)),
            "boundary_reason": None,
            "error": str(e)
        }]


def process_locomo_data(
    input_path: str,
    output_path: str,
    model: str = "gpt-4o",
    temperature: float = 0.3,
    limit: Optional[int] = None,
    start: int = 0
):
    """
    Process Locomo dataset and add topic segmentation.
    
    Args:
        input_path: Path to input JSON file
        output_path: Path to save output JSON file
        model: OpenAI model to use
        temperature: Temperature for generation
        limit: Optional limit on number of conversations to process (None = all)
        start: Start index (default: 0)
    """
    print(f"Loading data from {input_path}...")
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_convs = len(data)
    print(f"Total conversations in dataset: {total_convs}")
    
    # Apply start and limit
    if limit is not None:
        end = min(start + limit, total_convs)
        data = data[start:end]
        print(f"Processing conversations {start} to {end-1} ({len(data)} conversations)...")
    elif start > 0:
        data = data[start:]
        print(f"Processing conversations from {start} to end ({len(data)} conversations)...")
    else:
        print(f"Processing all {len(data)} conversations...")
    
    processed_data = []
    
    for conv in tqdm(data, desc="Segmenting conversations"):
        conv_id = conv.get("conv_id", "unknown")
        qas = conv.get("qas", [])
        dialogs = conv.get("dialogs", [])
        
        segmented_dialogs = []
        
        for dialog in dialogs:
            session_id = dialog.get("session_id", "unknown")
            datetime_str = dialog.get("datetime", "")
            messages = dialog.get("messages", [])
            
            # Skip empty sessions
            if not messages:
                segmented_dialogs.append({
                    "session_id": session_id,
                    "datetime": datetime_str,
                    "messages": messages,
                    "segments": []
                })
                continue
            
            # Perform segmentation
            segments = segment_dialogue_with_llm(
                messages=messages,
                model=model,
                temperature=temperature
            )
            
            segmented_dialogs.append({
                "session_id": session_id,
                "datetime": datetime_str,
                "messages": messages,
                "segments": segments
            })
        
        processed_data.append({
            "conv_id": conv_id,
            "qas": qas,
            "dialogs": segmented_dialogs
        })
    
    # Save results
    print(f"Saving segmented data to {output_path}...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, indent=4, ensure_ascii=False)
    
    print(f"Done! Processed {len(processed_data)} conversations.")
    
    # Print statistics
    total_sessions = sum(len(conv["dialogs"]) for conv in processed_data)
    total_segments = sum(
        len(dialog["segments"]) 
        for conv in processed_data 
        for dialog in conv["dialogs"]
    )
    
    print(f"\nStatistics:")
    print(f"  Total conversations: {len(processed_data)}")
    print(f"  Total sessions: {total_sessions}")
    print(f"  Total segments: {total_segments}")
    print(f"  Average segments per session: {total_segments / total_sessions:.2f}")


def main():
    parser = argparse.ArgumentParser(
        description="Perform topic segmentation on Locomo dialogue dataset",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process first 2 conversations (testing)
  python topic_segmentation.py --limit 2
  
  # Process conversations 10-15
  python topic_segmentation.py --start 10 --limit 5
  
  # Use Gemini with custom base URL (set in .env)
  python topic_segmentation.py --model gemini-1.5-flash --limit 2
  
  # Process all with specific model
  python topic_segmentation.py --model gpt-4o
        """
    )
    parser.add_argument(
        "--input",
        type=str,
        default="/home/hungpv/projects/memory_data/processed_data/locomo_processed_data.json",
        help="Path to input Locomo JSON file"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="/home/hungpv/projects/memory_data/processed_data/locomo_segmented_data.json",
        help="Path to output segmented JSON file"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Model to use (default: from .env or gpt-4o-mini)"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=None,
        help="Temperature for generation (default: from .env or 0.3)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Number of conversations to process (default: from .env or all). Use for testing or large datasets."
    )
    parser.add_argument(
        "--start",
        type=int,
        default=0,
        help="Start index for processing (default: 0)"
    )
    
    args = parser.parse_args()
    
    # Get configuration from .env or use defaults
    model = args.model or os.environ.get("DEFAULT_MODEL", "gpt-4o-mini")
    temperature = args.temperature if args.temperature is not None else float(os.environ.get("DEFAULT_TEMPERATURE", "0.3"))
    limit = args.limit
    if limit is None and os.environ.get("PROCESS_LIMIT"):
        limit = int(os.environ.get("PROCESS_LIMIT"))
    
    # Check for API key
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found")
        print("\nPlease either:")
        print("  1. Create .env file from env.example and set your API key")
        print("  2. Set environment variable: export OPENAI_API_KEY='your-api-key'")
        print("\nFor Gemini, also set OPENAI_BASE_URL in .env file")
        return
    
    # Print configuration
    print("\n" + "="*70)
    print("CONFIGURATION")
    print("="*70)
    print(f"Model: {model}")
    print(f"Temperature: {temperature}")
    print(f"Start index: {args.start}")
    print(f"Limit: {limit if limit else 'None (process all)'}")
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    if os.environ.get("OPENAI_BASE_URL"):
        print(f"Base URL: {os.environ.get('OPENAI_BASE_URL')}")
    print("="*70 + "\n")
    
    try:
        process_locomo_data(
            input_path=args.input,
            output_path=args.output,
            model=model,
            temperature=temperature,
            limit=limit,
            start=args.start
        )
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("  1. Check your API key is correct")
        print("  2. Verify base URL if using custom endpoint")
        print("  3. Ensure model name is correct")
        raise


if __name__ == "__main__":
    main()

