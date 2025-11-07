import json
import os
from pathlib import Path
from typing import List, Dict, Any
from openai import OpenAI
from tqdm import tqdm
import argparse
import time
from dotenv import load_dotenv

load_dotenv()

from topic_segmentation import segment_dialogue_with_llm, get_openai_client

client = get_openai_client()


def process_single_conversation(
    conv: Dict[str, Any],
    model: str = "gpt-4o",
    temperature: float = 0.3,
    retry_delay: float = 1.0,
    max_retries: int = 3
) -> Dict[str, Any]:
    """
    Process a single conversation with retry logic.
    
    Args:
        conv: Conversation data
        model: OpenAI model to use
        temperature: Temperature for generation
        retry_delay: Delay between retries (seconds)
        max_retries: Maximum number of retries
        
    Returns:
        Processed conversation with segments
    """
    conv_id = conv.get("conv_id", "unknown")
    qas = conv.get("qas", [])
    dialogs = conv.get("dialogs", [])
    
    segmented_dialogs = []
    
    for dialog in dialogs:
        session_id = dialog.get("session_id", "unknown")
        datetime_str = dialog.get("datetime", "")
        messages = dialog.get("messages", [])
        
        if not messages:
            segmented_dialogs.append({
                "session_id": session_id,
                "datetime": datetime_str,
                "messages": messages,
                "segments": []
            })
            continue
        
        segments = None
        for attempt in range(max_retries):
            try:
                segments = segment_dialogue_with_llm(
                    messages=messages,
                    model=model,
                    temperature=temperature
                )
                break  
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"  ⚠️  Retry {attempt + 1}/{max_retries} for {conv_id}/{session_id}: {e}")
                    time.sleep(retry_delay * (attempt + 1))  
                else:
                    print(f"  ❌ Failed after {max_retries} attempts for {conv_id}/{session_id}: {e}")
                    segments = [{
                        "segment_id": "seg_1",
                        "title": "Full conversation (segmentation failed)",
                        "summary": f"Segmentation failed: {str(e)}",
                        "key_entities": [],
                        "salient_facts": [],
                        "turn_indices": list(range(1, len(messages) + 1)),
                        "boundary_reason": None,
                        "error": str(e)
                    }]
        
        segmented_dialogs.append({
            "session_id": session_id,
            "datetime": datetime_str,
            "messages": messages,
            "segments": segments
        })
    
    return {
        "conv_id": conv_id,
        "qas": qas,
        "dialogs": segmented_dialogs
    }


def process_locomo_batch(
    input_path: str,
    output_dir: str,
    model: str = "gpt-4o",
    temperature: float = 0.3,
    start_idx: int = 0,
    end_idx: int = None,
    retry_delay: float = 1.0,
    max_retries: int = 3
):
    """
    Process Locomo dataset in batch mode, saving each conversation separately.
    
    Args:
        input_path: Path to input JSON file
        output_dir: Directory to save output files
        model: OpenAI model to use
        temperature: Temperature for generation
        start_idx: Start index for processing
        end_idx: End index for processing (None for all)
        retry_delay: Delay between retries
        max_retries: Maximum retries per session
    """
    print(f"Loading data from {input_path}...")
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if end_idx is None:
        end_idx = len(data)
    
    data_to_process = data[start_idx:end_idx]
    print(f"Processing conversations {start_idx} to {end_idx} ({len(data_to_process)} total)...")
    
    os.makedirs(output_dir, exist_ok=True)
    
    total_processed = 0
    total_failed = 0
    total_segments = 0
    
    for i, conv in enumerate(tqdm(data_to_process, desc="Segmenting conversations")):
        conv_id = conv.get("conv_id", f"conv_{start_idx + i}")
        output_path = os.path.join(output_dir, f"locomo_{conv_id}_segmented.json")
        
        if os.path.exists(output_path):
            print(f"  ⏭️  Skipping {conv_id} (already exists)")
            continue
        
        try:
            processed_conv = process_single_conversation(
                conv,
                model=model,
                temperature=temperature,
                retry_delay=retry_delay,
                max_retries=max_retries
            )
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(processed_conv, f, indent=4, ensure_ascii=False)
            
            num_segments = sum(
                len(dialog["segments"]) 
                for dialog in processed_conv["dialogs"]
            )
            total_segments += num_segments
            total_processed += 1
            
        except Exception as e:
            print(f"  ❌ Failed to process {conv_id}: {e}")
            total_failed += 1
    
    print("\n" + "="*70)
    print("BATCH PROCESSING SUMMARY")
    print("="*70)
    print(f"Total processed: {total_processed}")
    print(f"Total failed: {total_failed}")
    print(f"Total segments created: {total_segments}")
    print(f"Average segments per conversation: {total_segments / total_processed:.2f}" if total_processed > 0 else "N/A")
    print(f"Output directory: {output_dir}")
    print("="*70)


def merge_batch_results(
    batch_dir: str,
    output_path: str
):
    """
    Merge individual conversation files into a single JSON file.
    
    Args:
        batch_dir: Directory containing individual conversation files
        output_path: Path to save merged JSON file
    """
    print(f"Merging results from {batch_dir}...")
    
    json_files = sorted(Path(batch_dir).glob("locomo_*_segmented.json"))
    
    if not json_files:
        print(f"⚠️  No files found in {batch_dir}")
        return
    
    print(f"Found {len(json_files)} files to merge...")
    
    merged_data = []
    
    for json_file in tqdm(json_files, desc="Merging files"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                conv_data = json.load(f)
                merged_data.append(conv_data)
        except Exception as e:
            print(f"  ⚠️  Failed to read {json_file}: {e}")
    
    print(f"Saving merged data to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Merged {len(merged_data)} conversations to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Batch process Locomo dataset for topic segmentation"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    process_parser = subparsers.add_parser('process', help='Process conversations')
    process_parser.add_argument(
        "--input",
        type=str,
        default="/home/hungpv/projects/memory_data/processed_data/locomo_processed_data.json",
        help="Path to input Locomo JSON file"
    )
    process_parser.add_argument(
        "--output-dir",
        type=str,
        default="/home/hungpv/projects/memory_data/processed_data/locomo_segmented_batch",
        help="Directory to save individual conversation files"
    )
    process_parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o",
        help="OpenAI model to use"
    )
    process_parser.add_argument(
        "--temperature",
        type=float,
        default=0.3,
        help="Temperature for generation"
    )
    process_parser.add_argument(
        "--start",
        type=int,
        default=0,
        help="Start index"
    )
    process_parser.add_argument(
        "--end",
        type=int,
        default=None,
        help="End index (None for all)"
    )
    process_parser.add_argument(
        "--retry-delay",
        type=float,
        default=1.0,
        help="Delay between retries (seconds)"
    )
    process_parser.add_argument(
        "--max-retries",
        type=int,
        default=3,
        help="Maximum retries per session"
    )
    
    merge_parser = subparsers.add_parser('merge', help='Merge batch results')
    merge_parser.add_argument(
        "--batch-dir",
        type=str,
        default="/home/hungpv/projects/memory_data/processed_data/locomo_segmented_batch",
        help="Directory containing individual conversation files"
    )
    merge_parser.add_argument(
        "--output",
        type=str,
        default="/home/hungpv/projects/memory_data/processed_data/locomo_segmented_merged.json",
        help="Path to save merged JSON file"
    )
    
    args = parser.parse_args()
    
    if args.command == 'process':
        if not os.environ.get("OPENAI_API_KEY"):
            print("❌ Error: OPENAI_API_KEY not found")
            print("\nPlease either:")
            print("  1. Create .env file from env.example and set your API key")
            print("  2. Set environment variable: export OPENAI_API_KEY='your-api-key'")
            print("\nFor Gemini, also set OPENAI_BASE_URL in .env file")
            return
        
        process_locomo_batch(
            input_path=args.input,
            output_dir=args.output_dir,
            model=args.model,
            temperature=args.temperature,
            start_idx=args.start,
            end_idx=args.end,
            retry_delay=args.retry_delay,
            max_retries=args.max_retries
        )
    
    elif args.command == 'merge':
        merge_batch_results(
            batch_dir=args.batch_dir,
            output_path=args.output
        )
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

