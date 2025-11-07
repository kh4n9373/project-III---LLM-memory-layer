import json
import argparse
from typing import List, Dict, Any
from collections import Counter
import statistics


def load_segmented_data(filepath: str) -> List[Dict[str, Any]]:
    """Load segmented data from JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def analyze_statistics(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze segmentation statistics.
    
    Returns:
        Dictionary with various statistics
    """
    total_convs = len(data)
    total_sessions = 0
    total_segments = 0
    total_messages = 0
    
    segments_per_session = []
    messages_per_segment = []
    segment_titles = []
    key_entities_count = []
    
    for conv in data:
        for dialog in conv.get("dialogs", []):
            total_sessions += 1
            messages = dialog.get("messages", [])
            segments = dialog.get("segments", [])
            
            total_messages += len(messages)
            total_segments += len(segments)
            
            if segments:
                segments_per_session.append(len(segments))
            
            for segment in segments:
                segment_titles.append(segment.get("title", ""))
                
                turn_indices = segment.get("turn_indices", [])
                messages_per_segment.append(len(turn_indices))
                
                entities = segment.get("key_entities", [])
                key_entities_count.append(len(entities))
    
    stats = {
        "total_conversations": total_convs,
        "total_sessions": total_sessions,
        "total_segments": total_segments,
        "total_messages": total_messages,
        
        "avg_sessions_per_conv": total_sessions / total_convs if total_convs > 0 else 0,
        "avg_segments_per_session": statistics.mean(segments_per_session) if segments_per_session else 0,
        "median_segments_per_session": statistics.median(segments_per_session) if segments_per_session else 0,
        
        "avg_messages_per_segment": statistics.mean(messages_per_segment) if messages_per_segment else 0,
        "median_messages_per_segment": statistics.median(messages_per_segment) if messages_per_segment else 0,
        "min_messages_per_segment": min(messages_per_segment) if messages_per_segment else 0,
        "max_messages_per_segment": max(messages_per_segment) if messages_per_segment else 0,
        
        "avg_entities_per_segment": statistics.mean(key_entities_count) if key_entities_count else 0,
        
        "segments_per_session_distribution": Counter(segments_per_session),
        "messages_per_segment_distribution": Counter(messages_per_segment),
    }
    
    return stats


def print_statistics(stats: Dict[str, Any]):
    """Pretty print statistics."""
    print("\n" + "="*70)
    print("TOPIC SEGMENTATION STATISTICS")
    print("="*70)
    
    print("\n📊 OVERVIEW:")
    print(f"  Total conversations: {stats['total_conversations']}")
    print(f"  Total sessions: {stats['total_sessions']}")
    print(f"  Total segments: {stats['total_segments']}")
    print(f"  Total messages: {stats['total_messages']}")
    
    print("\n📈 AVERAGES:")
    print(f"  Avg sessions per conversation: {stats['avg_sessions_per_conv']:.2f}")
    print(f"  Avg segments per session: {stats['avg_segments_per_session']:.2f}")
    print(f"  Median segments per session: {stats['median_segments_per_session']:.1f}")
    
    print("\n💬 MESSAGES PER SEGMENT:")
    print(f"  Average: {stats['avg_messages_per_segment']:.2f}")
    print(f"  Median: {stats['median_messages_per_segment']:.1f}")
    print(f"  Min: {stats['min_messages_per_segment']}")
    print(f"  Max: {stats['max_messages_per_segment']}")
    
    print("\n🏷️  ENTITIES:")
    print(f"  Avg entities per segment: {stats['avg_entities_per_segment']:.2f}")
    
    print("\n📊 DISTRIBUTION - Segments per session:")
    seg_dist = stats['segments_per_session_distribution']
    for num_segments in sorted(seg_dist.keys())[:10]:
        count = seg_dist[num_segments]
        print(f"  {num_segments} segments: {count} sessions")
    
    print("\n📊 DISTRIBUTION - Messages per segment:")
    msg_dist = stats['messages_per_segment_distribution']
    for num_msgs in sorted(msg_dist.keys())[:15]:
        count = msg_dist[num_msgs]
        bar = "█" * min(count // 5, 50)
        print(f"  {num_msgs:2d} messages: {count:4d} segments {bar}")
    
    print("\n" + "="*70)


def export_readable_segments(
    data: List[Dict[str, Any]], 
    output_path: str,
    max_convs: int = None
):
    """
    Export segments in a human-readable format.
    
    Args:
        data: Segmented data
        output_path: Path to save readable text file
        max_convs: Maximum conversations to export (None for all)
    """
    lines = []
    lines.append("="*80)
    lines.append("LOCOMO TOPIC SEGMENTATION - READABLE EXPORT")
    lines.append("="*80)
    lines.append("")
    
    convs_to_process = data[:max_convs] if max_convs else data
    
    for conv in convs_to_process:
        conv_id = conv.get("conv_id", "unknown")
        lines.append(f"\n{'='*80}")
        lines.append(f"CONVERSATION: {conv_id}")
        lines.append(f"{'='*80}")
        
        for dialog in conv.get("dialogs", []):
            session_id = dialog.get("session_id", "unknown")
            datetime_str = dialog.get("datetime", "")
            segments = dialog.get("segments", [])
            messages = dialog.get("messages", [])
            
            lines.append(f"\n  SESSION: {session_id}")
            lines.append(f"  DateTime: {datetime_str}")
            lines.append(f"  Total Messages: {len(messages)}")
            lines.append(f"  Total Segments: {len(segments)}")
            lines.append(f"  {'-'*76}")
            
            for seg in segments:
                seg_id = seg.get("segment_id", "unknown")
                title = seg.get("title", "Untitled")
                summary = seg.get("summary", "")
                entities = seg.get("key_entities", [])
                facts = seg.get("salient_facts", [])
                turn_indices = seg.get("turn_indices", [])
                boundary = seg.get("boundary_reason", "N/A")
                
                lines.append(f"\n    [{seg_id}] {title}")
                lines.append(f"    Turns: {turn_indices}")
                lines.append(f"    Summary: {summary}")
                lines.append(f"    Entities: {', '.join(entities)}")
                lines.append(f"    Facts: {', '.join(facts)}")
                if boundary:
                    lines.append(f"    Boundary Reason: {boundary}")
                
                # Show the actual messages in this segment
                lines.append(f"    Messages:")
                for turn_idx in turn_indices:
                    if 1 <= turn_idx <= len(messages):
                        msg = messages[turn_idx - 1]
                        role = msg.get("role", "Unknown")
                        content = msg.get("content", "")
                        content_preview = content[:100] + "..." if len(content) > 100 else content
                        lines.append(f"      [{turn_idx}] {role}: {content_preview}")
                
                lines.append("")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    
    print(f"\n✅ Readable export saved to: {output_path}")


def validate_segmentation(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validate segmentation quality.
    
    Checks for:
    - Segments with too few messages
    - Missing turn indices
    - Overlapping segments
    - Gaps in coverage
    """
    issues = {
        "too_few_messages": [],  
        "missing_turns": [],     
        "coverage_gaps": [],      
        "overlapping_segments": [], 
    }
    
    for conv in data:
        conv_id = conv.get("conv_id", "unknown")
        
        for dialog in conv.get("dialogs", []):
            session_id = dialog.get("session_id", "unknown")
            messages = dialog.get("messages", [])
            segments = dialog.get("segments", [])
            
            total_turns = len(messages)
            covered_turns = set()
            
            for seg in segments:
                turn_indices = seg.get("turn_indices", [])
                seg_id = seg.get("segment_id", "unknown")
                
                if not turn_indices:
                    issues["missing_turns"].append({
                        "conv_id": conv_id,
                        "session_id": session_id,
                        "segment_id": seg_id
                    })
                    continue
                
                if len(turn_indices) < 2:
                    issues["too_few_messages"].append({
                        "conv_id": conv_id,
                        "session_id": session_id,
                        "segment_id": seg_id,
                        "num_messages": len(turn_indices)
                    })
                
                turn_set = set(turn_indices)
                overlap = covered_turns & turn_set
                if overlap:
                    issues["overlapping_segments"].append({
                        "conv_id": conv_id,
                        "session_id": session_id,
                        "segment_id": seg_id,
                        "overlapping_turns": sorted(overlap)
                    })
                
                covered_turns.update(turn_set)
            
            expected_turns = set(range(1, total_turns + 1))
            missing_turns = expected_turns - covered_turns
            if missing_turns:
                issues["coverage_gaps"].append({
                    "conv_id": conv_id,
                    "session_id": session_id,
                    "total_turns": total_turns,
                    "covered_turns": len(covered_turns),
                    "missing_turns": sorted(missing_turns)
                })
    
    return issues


def print_validation_report(issues: Dict[str, Any]):
    """Print validation report."""
    print("\n" + "="*70)
    print("SEGMENTATION VALIDATION REPORT")
    print("="*70)
    
    total_issues = sum(len(v) for v in issues.values())
    
    if total_issues == 0:
        print("\n✅ No issues found! Segmentation looks good.")
    else:
        print(f"\n⚠️  Found {total_issues} total issues:\n")
        
        if issues["too_few_messages"]:
            print(f"  ⚠️  Segments with < 2 messages: {len(issues['too_few_messages'])}")
            for item in issues["too_few_messages"][:5]:
                print(f"      - {item['conv_id']}/{item['session_id']}/{item['segment_id']}: {item['num_messages']} message(s)")
        
        if issues["missing_turns"]:
            print(f"  ⚠️  Segments with missing turn indices: {len(issues['missing_turns'])}")
            for item in issues["missing_turns"][:5]:
                print(f"      - {item['conv_id']}/{item['session_id']}/{item['segment_id']}")
        
        if issues["overlapping_segments"]:
            print(f"  ⚠️  Overlapping segments: {len(issues['overlapping_segments'])}")
            for item in issues["overlapping_segments"][:5]:
                print(f"      - {item['conv_id']}/{item['session_id']}/{item['segment_id']}: turns {item['overlapping_turns']}")
        
        if issues["coverage_gaps"]:
            print(f"  ⚠️  Sessions with coverage gaps: {len(issues['coverage_gaps'])}")
            for item in issues["coverage_gaps"][:5]:
                print(f"      - {item['conv_id']}/{item['session_id']}: {item['covered_turns']}/{item['total_turns']} covered")
    
    print("\n" + "="*70)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze topic segmentation results"
    )
    parser.add_argument(
        "--input",
        type=str,
        default="/home/hungpv/projects/memory_data/processed_data/locomo_segmented_data.json",
        help="Path to segmented JSON file"
    )
    parser.add_argument(
        "--export",
        type=str,
        default=None,
        help="Export readable format to this file"
    )
    parser.add_argument(
        "--max-export",
        type=int,
        default=3,
        help="Maximum conversations to export (default: 3)"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Run validation checks"
    )
    
    args = parser.parse_args()
    
    print(f"Loading data from {args.input}...")
    data = load_segmented_data(args.input)
    
    stats = analyze_statistics(data)
    print_statistics(stats)
    
    if args.validate:
        issues = validate_segmentation(data)
        print_validation_report(issues)
    
    if args.export:
        export_readable_segments(data, args.export, max_convs=args.max_export)


if __name__ == "__main__":
    main()

