# 🎯 Topic Segmentation for Locomo Dataset

Hệ thống tự động phân đoạn (segment) các hội thoại dài thành các topics có ngữ nghĩa liên kết.

---

## ⚡ Quick Start (3 phút)

```bash
# 1. Install
pip install -r requirements_segmentation.txt

# 2. Setup .env file
cp env.example .env
# Edit .env và paste API key của bạn

# 3. Test
python test_segmentation.py

# 4. Run (test with 2 conversations)
python topic_segmentation.py --limit 2

# 5. Analyze
python analyze_segmentation.py --validate
```

**📖 Đọc hướng dẫn setup chi tiết**: [SETUP_WITH_ENV.md](SETUP_WITH_ENV.md)

---

## 📚 Documentation

### 🌟 **Bắt đầu tại đây**
- **[QUICKSTART_SEGMENTATION.md](QUICKSTART_SEGMENTATION.md)** ⭐ - Hướng dẫn nhanh, workflows, examples

### 📖 **Tài liệu chi tiết**
- **[SETUP_WITH_ENV.md](SETUP_WITH_ENV.md)** 🔧 - Setup với .env và Gemini
- **[TOPIC_SEGMENTATION_SUMMARY.md](TOPIC_SEGMENTATION_SUMMARY.md)** - Tổng quan hệ thống
- **[TOPIC_SEGMENTATION_README.md](TOPIC_SEGMENTATION_README.md)** - Full documentation
- **[SEGMENTATION_INDEX.md](SEGMENTATION_INDEX.md)** - Danh sách tất cả files
- **[CHANGELOG_SEGMENTATION.md](CHANGELOG_SEGMENTATION.md)** - Version history

---

## 🌟 New in v1.1

- ✅ **Environment file support** (.env) - No more export commands!
- ✅ **Gemini API support** - Use Google's Gemini models
- ✅ **Custom base URL** - Compatible với any OpenAI-like API
- ✅ **Better config** - Set defaults in .env, override với command line
- ✅ **Improved limits** - `--start` và `--limit` cho flexible range processing

---

## 🔧 Tools

| Script | Purpose | Usage |
|--------|---------|-------|
| `topic_segmentation.py` | Main segmentation | `python topic_segmentation.py` |
| `segment_locomo_batch.py` | Batch processing | `python segment_locomo_batch.py process` |
| `analyze_segmentation.py` | Analysis & validation | `python analyze_segmentation.py --validate` |
| `test_segmentation.py` | Test setup | `python test_segmentation.py` |

---

## 📊 Example Output

**Input:** Dialogue with multiple topics

**Output:** Segmented dialogue with:
- `segment_id`: Unique identifier
- `title`: Short descriptive title
- `summary`: 2-3 sentences preserving key details
- `key_entities`: People, dates, events
- `salient_facts`: Key facts in key-value format
- `turn_indices`: Turn numbers in segment
- `boundary_reason`: Why segment starts here

See [segmentation_example_output.json](segmentation_example_output.json) for complete example.

---

## 🎯 Common Commands

### Setup .env file (one-time)
```bash
cp env.example .env
# Edit .env với your API key và settings
```

### Test with sample data
```bash
python test_segmentation.py
```

### Segment 2 conversations (testing)
```bash
# Sử dụng config từ .env
python topic_segmentation.py --limit 2

# Override model nếu cần
python topic_segmentation.py --limit 2 --model gemini-1.5-flash
```

### Segment specific range
```bash
# Conversations 0-4
python topic_segmentation.py --start 0 --limit 5

# Conversations 10-19
python topic_segmentation.py --start 10 --limit 10
```

### Segment full dataset
```bash
# Sử dụng config từ .env
python topic_segmentation.py
```

### Batch processing (recommended for production)
```bash
# Process
python segment_locomo_batch.py process \
    --input ./processed_data/locomo_processed_data.json \
    --output-dir ./processed_data/locomo_segmented_batch \
    --model gpt-4o-mini

# Merge results
python segment_locomo_batch.py merge \
    --batch-dir ./processed_data/locomo_segmented_batch \
    --output ./processed_data/locomo_segmented_merged.json
```

### Analyze results
```bash
# Statistics
python analyze_segmentation.py \
    --input ./processed_data/locomo_segmented_data.json

# Validate quality
python analyze_segmentation.py \
    --input ./processed_data/locomo_segmented_data.json \
    --validate

# Export readable format
python analyze_segmentation.py \
    --input ./processed_data/locomo_segmented_data.json \
    --export ./analysis/segments_readable.txt \
    --max-export 5
```

---

## 📁 Files Created

### Scripts (4 files)
- `topic_segmentation.py` (11K) - Main segmentation script
- `segment_locomo_batch.py` (11K) - Batch processing
- `analyze_segmentation.py` (14K) - Analysis tools
- `test_segmentation.py` (4.4K) - Test script

### Documentation (6 files)
- `README_TOPIC_SEGMENTATION.md` - Main README ⭐
- `QUICKSTART_SEGMENTATION.md` (6.3K) - Quick start guide
- `SETUP_WITH_ENV.md` 🆕 - Setup with .env & Gemini
- `TOPIC_SEGMENTATION_README.md` (8.3K) - Full documentation
- `TOPIC_SEGMENTATION_SUMMARY.md` (12K) - System overview
- `SEGMENTATION_INDEX.md` (9.9K) - File index
- `CHANGELOG_SEGMENTATION.md` 🆕 - Version history

### Config & Examples (3 files)
- `requirements_segmentation.txt` - Dependencies (with dotenv)
- `env.example` 🆕 - Environment configuration template
- `segmentation_example_output.json` (7.7K) - Example output

**Total: 13 files (~120KB)**

---

## 🎯 Segmentation Methodology

### Cut Criteria (when to create new segment):
1. **Intent shift** - Goal changes (career → family)
2. **Entity/Topic shift** - Main subject changes
3. **Temporal cue** - Time change ("yesterday", "next week")
4. **Resolution point** - Task/topic concluded

### Guidelines:
- ✅ Preserve names, dates, numbers
- ✅ 2-3 sentence summaries
- ✅ Min 2 turns per segment
- ❌ Don't cut on fillers ("uhm", "ok")
- ❌ Avoid over-segmentation

---

## 💡 Tips

1. **Use .env file**: Easier than export commands, can commit env.example
2. **Start small**: Always test với `--limit 2` first
3. **Try Gemini**: Cheaper và faster than OpenAI cho testing
4. **Use batch mode**: For production/large datasets
5. **Validate quality**: Run analysis after segmentation
6. **Monitor costs**: Track API usage dashboard
7. **Choose right model**:
   - `gemini-1.5-flash` - Cheapest, fastest ⭐
   - `gpt-4o-mini` - Fast, good quality
   - `gpt-4o` - Balanced
   - `gemini-1.5-pro` - High quality
   - `gpt-4-turbo` - Best quality, expensive

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| API key error | Check `.env` file has `OPENAI_API_KEY` |
| Base URL error | Set `OPENAI_BASE_URL` in `.env` for Gemini |
| Model not found | Check model name matches API (gemini-1.5-flash vs gpt-4o) |
| Rate limit | Use `--retry-delay 2.0` or wait |
| Bad segments | Adjust `--temperature` (try 0.2 or 0.4) |
| Incomplete | Run `analyze_segmentation.py --validate` |

---

## 📊 Expected Performance

For Locomo dataset (~10 conversations, ~100 sessions):

- **Time**: 5-30 minutes (depends on model)
- **Cost**: 
  - Gemini Flash: ~$0.10-0.30 (cheapest!) ⭐
  - GPT-4o-mini: ~$0.50-2.00
  - GPT-4o: ~$5-15
- **Quality**: 2-4 segments/session, 95%+ coverage

---

## 🔄 Workflow

```
Install → Setup .env → Test → Segment (small) → Validate → Segment (full) → Analyze
```

---

## 📖 Next Steps

1. **Setup**: [SETUP_WITH_ENV.md](SETUP_WITH_ENV.md) - Setup .env với Gemini hoặc OpenAI
2. **Quick Start**: [QUICKSTART_SEGMENTATION.md](QUICKSTART_SEGMENTATION.md) - Detailed workflows
3. **Deep Dive**: [TOPIC_SEGMENTATION_README.md](TOPIC_SEGMENTATION_README.md) - Full methodology
4. **Reference**: [SEGMENTATION_INDEX.md](SEGMENTATION_INDEX.md) - File index

---

## ✨ Features

✅ LLM-powered semantic segmentation  
✅ **Environment file support (.env)** 🆕  
✅ **Multi-API support (OpenAI, Gemini, Local)** 🆕  
✅ Multiple processing modes (single/batch/parallel)  
✅ Comprehensive validation tools  
✅ Human-readable exports  
✅ Production-ready với error handling  
✅ Complete documentation  

---

## 🚀 Ready to Start?

```bash
# Quick start
pip install -r requirements_segmentation.txt
cp env.example .env
# Edit .env, then:
python test_segmentation.py
python topic_segmentation.py --limit 2
```

**📖 Full guide**: [SETUP_WITH_ENV.md](SETUP_WITH_ENV.md)

---

**Version**: 1.1 | **Created**: November 2025 | **Status**: ✅ Ready to use

