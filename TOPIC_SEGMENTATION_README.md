# Topic Segmentation for Locomo Dataset

Hệ thống topic segmentation tự động cho dữ liệu hội thoại (dialogue) từ dataset Locomo.

## 📋 Mục đích

Split các hội thoại dài thành các segments (đoạn) có ngữ nghĩa liên kết - mỗi segment gom nhóm các turns (lượt) phục vụ cùng một intent/topic.

### Lợi ích:
- Giảm nhiễu (noise) khi xử lý
- Tạo ra các đơn vị storage/retrieval tốt hơn
- Inputs mạnh hơn cho summarization, Information Extraction
- Hỗ trợ cho graph/RAG systems

## 🚀 Cài đặt

### Requirements

```bash
pip install openai tqdm
```

### Cấu hình API Key

```bash
export OPENAI_API_KEY='your-openai-api-key'
```

## 📖 Cách sử dụng

### 1. Chạy Topic Segmentation

Xử lý toàn bộ dataset:

```bash
python topic_segmentation.py \
    --input /home/hungpv/projects/memory_data/processed_data/locomo_processed_data.json \
    --output /output/segmentation/locomo_segmented.json \
    --model gpt-4o \
    --temperature 0.3
```

Test với một vài conversations đầu tiên:

```bash
python topic_segmentation.py \
    --input ./processed_data/locomo_processed_data.json \
    --output ./processed_data/locomo_segmented_data.json \
    --limit 2
```

#### Arguments:

- `--input`: Đường dẫn file JSON input (default: locomo_processed_data.json)
- `--output`: Đường dẫn file JSON output (default: locomo_segmented_data.json)
- `--model`: Model OpenAI sử dụng (default: gpt-4o)
  - Options: gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-3.5-turbo
- `--temperature`: Temperature cho generation (default: 0.3)
  - Range: 0.0 - 1.0 (thấp hơn = consistent hơn)
- `--limit`: Giới hạn số conversations xử lý (for testing)

### 2. Phân tích kết quả

Xem thống kê:

```bash
python analyze_segmentation.py \
    --input ./processed_data/locomo_segmented_data.json
```

Validate chất lượng segmentation:

```bash
python analyze_segmentation.py \
    --input ./processed_data/locomo_segmented_data.json \
    --validate
```

Export ra format dễ đọc:

```bash
python analyze_segmentation.py \
    --input ./processed_data/locomo_segmented_data.json \
    --export ./analysis/segments_readable.txt \
    --max-export 5
```

## 📊 Output Schema

Mỗi segment bao gồm:

```json
{
  "segment_id": "seg_1",
  "title": "Short descriptive title",
  "summary": "2-3 sentence summary with names, dates, and key details preserved",
  "key_entities": ["person", "date", "location", "event"],
  "salient_facts": ["fact1=value1", "fact2=value2"],
  "turn_indices": [1, 2, 3, 4],
  "boundary_reason": "Why this segment starts here (null for first segment)"
}
```

### Ví dụ Output Structure:

```json
[
  {
    "conv_id": "conv-26",
    "qas": [...],
    "dialogs": [
      {
        "session_id": "session_1",
        "datetime": "1:56 pm on 8 May, 2023",
        "messages": [
          {
            "role": "Caroline",
            "content": "Hey Mel! Good to see you!"
          },
          ...
        ],
        "segments": [
          {
            "segment_id": "seg_1",
            "title": "LGBTQ support group experience",
            "summary": "Caroline shares her powerful experience at an LGBTQ support group...",
            "key_entities": ["Caroline", "LGBTQ support group", "transgender"],
            "salient_facts": ["attended_support_group=true", "date=7 May 2023"],
            "turn_indices": [1, 2, 3, 4, 5],
            "boundary_reason": null
          },
          ...
        ]
      }
    ]
  }
]
```

## 🎯 Segmentation Criteria

### Khi nào tạo segment mới (Cut criteria):

1. **Intent shift**: Mục đích cuộc trò chuyện thay đổi
   - Ví dụ: từ thảo luận về sự nghiệp → chuyển sang thảo luận về gia đình

2. **Entity/Topic shift**: Chủ đề chính thay đổi đáng kể
   - Ví dụ: từ nói về thesis → chuyển sang server crash

3. **Temporal cue**: Thay đổi thời gian rõ ràng
   - Ví dụ: "yesterday", "next week", "last month"

4. **Resolution point**: Một task/topic được kết thúc rõ ràng
   - Ví dụ: link được cung cấp và confirmed

### Lưu ý quan trọng:

- ❌ **KHÔNG** cắt segment cho fillers ("uhm", "ok", greetings)
- ❌ **KHÔNG** over-segment: ưu tiên ít segments lớn hơn nhiều segments nhỏ
- ✅ Mỗi segment phải có **ít nhất 2 turns**
- ✅ Giữ nguyên **names, dates, numbers** trong summaries
- ✅ Summaries nên **2-3 câu**

## 📈 Metrics & Validation

Script `analyze_segmentation.py` sẽ kiểm tra:

1. **Statistics**:
   - Số lượng segments per session
   - Số lượng messages per segment
   - Distribution của segments

2. **Validation checks**:
   - Segments có quá ít messages (< 2)
   - Segments thiếu turn_indices
   - Coverage gaps (turns không được cover)
   - Overlapping segments

## 🔧 Advanced Usage

### Custom Prompts

Bạn có thể chỉnh sửa prompt trong file `topic_segmentation.py`:

```python
SEGMENTATION_PROMPT = """
Your custom prompt here...
"""
```

### Batch Processing

Để xử lý nhiều files:

```bash
for file in ./data/*.json; do
    python topic_segmentation.py --input "$file" --output "./segmented/$(basename $file)"
done
```

### Using Different Models

Với GPT-4o-mini (nhanh hơn, rẻ hơn):
```bash
python topic_segmentation.py --model gpt-4o-mini
```

Với GPT-4-turbo (chất lượng cao hơn):
```bash
python topic_segmentation.py --model gpt-4-turbo
```

## 📝 Examples

### Example 1: Simple segmentation

**Input dialogue:**
```
[1] Caroline: Hey Mel! Good to see you!
[2] Melanie: Hey Caroline! What's up?
[3] Caroline: I went to an LGBTQ support group yesterday
[4] Melanie: That's cool! What happened?
[5] Caroline: The transgender stories were so inspiring!
[6] Melanie: What are your plans now?
[7] Caroline: I'm looking into counseling careers
```

**Output segments:**
```json
[
  {
    "segment_id": "seg_1",
    "title": "LGBTQ support group experience",
    "summary": "Caroline shares her experience attending an LGBTQ support group yesterday. She found the transgender stories particularly inspiring and powerful.",
    "key_entities": ["Caroline", "LGBTQ support group", "transgender", "yesterday"],
    "salient_facts": ["attended_support_group=true", "date=yesterday"],
    "turn_indices": [1, 2, 3, 4, 5],
    "boundary_reason": null
  },
  {
    "segment_id": "seg_2",
    "title": "Career planning in counseling",
    "summary": "Caroline discusses her future career plans, expressing interest in counseling field.",
    "key_entities": ["Caroline", "counseling", "career"],
    "salient_facts": ["career_interest=counseling"],
    "turn_indices": [6, 7],
    "boundary_reason": "Intent shift from sharing experience to career planning"
  }
]
```

## 🐛 Troubleshooting

### Error: "OPENAI_API_KEY environment variable not set"

**Solution:**
```bash
export OPENAI_API_KEY='sk-...'
```

### Error: Rate limit exceeded

**Solution:**
- Sử dụng `--limit` để xử lý ít conversations hơn
- Thêm retry logic hoặc sleep delay
- Upgrade OpenAI plan

### Segments quá dài/ngắn

**Solution:**
- Điều chỉnh temperature (thấp hơn = consistent hơn)
- Modify prompt để explicit hơn về segment size
- Thử model khác (gpt-4o thường tốt hơn gpt-3.5-turbo)

## 📚 Pipeline Integration

Recommended pipeline:

```
1. Load Locomo data
   ↓
2. Topic Segmentation (script này)
   ↓
3. Store segments {summary, facts, entities, timestamps}
   ↓
4. Index (vector embeddings + metadata)
   ↓
5. Build knowledge graph (optional)
   ↓
6. Retrieve by topic first → drill down to raw spans
```

## 💡 Tips & Best Practices

1. **Start with testing**: Luôn test với `--limit 2` trước khi chạy full dataset
2. **Monitor costs**: OpenAI API có phí, track usage của bạn
3. **Save intermediate results**: Backup output files thường xuyên
4. **Validate quality**: Chạy analysis script sau mỗi lần segmentation
5. **Iterate on prompts**: Fine-tune prompt nếu kết quả chưa như mong đợi

## 📞 Support

Nếu gặp vấn đề:
1. Check validation report: `--validate`
2. Review readable export để understand segments
3. Adjust temperature hoặc model
4. Modify prompt cho specific use case của bạn

---

**Author**: hungpv  
**Date**: November 2025  
**Version**: 1.0

