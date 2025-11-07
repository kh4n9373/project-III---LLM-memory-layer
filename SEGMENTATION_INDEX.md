# Topic Segmentation - File Index

Index của tất cả các files liên quan đến topic segmentation cho Locomo dataset.

---

## 📚 Documentation Files

### 1. `QUICKSTART_SEGMENTATION.md` ⭐ **BẮT ĐẦU TẠI ĐÂY**
- **Mục đích**: Hướng dẫn nhanh để bắt đầu (5-10 phút)
- **Nội dung**: Setup, các cách chạy, workflows phổ biến
- **Dành cho**: Người dùng muốn bắt đầu nhanh

### 2. `TOPIC_SEGMENTATION_README.md`
- **Mục đích**: Documentation đầy đủ và chi tiết
- **Nội dung**: Theory, schema, examples, troubleshooting, best practices
- **Dành cho**: Tìm hiểu sâu về segmentation methodology

### 3. `SEGMENTATION_INDEX.md` (file này)
- **Mục đích**: Tổng quan tất cả các files
- **Nội dung**: Danh sách files, mục đích, usage
- **Dành cho**: Navigation và reference

---

## 🔧 Core Scripts

### 4. `topic_segmentation.py` ⭐ **MAIN SCRIPT**
- **Mục đích**: Script chính để chạy topic segmentation
- **Input**: `locomo_processed_data.json`
- **Output**: `locomo_segmented_data.json`
- **Usage**:
  ```bash
  python topic_segmentation.py \
      --input ./processed_data/locomo_processed_data.json \
      --output ./output/segmentation/locomo_segmented_data.json \
      --limit 1
  ```
- **Features**:
  - Single-file processing
  - Automatic segmentation với LLM
  - Retry logic
  - Progress tracking
- **Dành cho**: Quick runs, testing, small datasets

### 5. `segment_locomo_batch.py` ⭐ **BATCH SCRIPT**
- **Mục đích**: Batch processing với fault tolerance
- **Input**: `locomo_processed_data.json`
- **Output**: Individual files per conversation + merged file
- **Usage**:
  ```bash
  # Process
  python segment_locomo_batch.py process \
      --input ./processed_data/locomo_processed_data.json \
      --output-dir ./processed_data/locomo_segmented_batch \
      --start 0 --end 10
  
  # Merge
  python segment_locomo_batch.py merge \
      --batch-dir ./processed_data/locomo_segmented_batch \
      --output ./processed_data/locomo_segmented_merged.json
  ```
- **Features**:
  - Process conversations individually
  - Skip already processed files
  - Exponential backoff retry
  - Resume capability
  - Merge results
- **Dành cho**: Production, large datasets, parallel processing

### 6. `analyze_segmentation.py`
- **Mục đích**: Analyze và validate segmentation results
- **Input**: Segmented data JSON
- **Output**: Statistics, validation report, readable export
- **Usage**:
  ```bash
  # Statistics
  python analyze_segmentation.py --input ./processed_data/locomo_segmented_data.json
  
  # Validate
  python analyze_segmentation.py --input ./processed_data/locomo_segmented_data.json --validate
  
  # Export readable
  python analyze_segmentation.py \
      --input ./processed_data/locomo_segmented_data.json \
      --export ./analysis/segments.txt \
      --max-export 5
  ```
- **Features**:
  - Distribution statistics
  - Validation checks (coverage, overlaps, etc.)
  - Human-readable export
  - Quality metrics
- **Dành cho**: Quality assurance, debugging, reporting

### 7. `test_segmentation.py`
- **Mục đích**: Test script để verify setup
- **Input**: Hardcoded test dialogue
- **Output**: Console output + `test_segmentation_output.json`
- **Usage**:
  ```bash
  python test_segmentation.py
  ```
- **Features**:
  - Test dialogue formatting
  - Test LLM segmentation
  - Validate API connection
  - Check output structure
- **Dành cho**: Initial setup verification, debugging

---

## 📋 Configuration Files

### 8. `requirements_segmentation.txt`
- **Mục đích**: Python dependencies
- **Nội dung**:
  ```
  openai>=1.3.0
  tqdm>=4.65.0
  ```
- **Usage**:
  ```bash
  pip install -r requirements_segmentation.txt
  ```

---

## 📊 Example Files

### 9. `segmentation_example_output.json`
- **Mục đích**: Example của output structure
- **Nội dung**: 1 conversation với 2 sessions đã được segmented
- **Dành cho**: Understanding output schema, reference

---

## 📁 Directory Structure

```
memory_data/
│
├── Documentation
│   ├── QUICKSTART_SEGMENTATION.md          ⭐ Start here
│   ├── TOPIC_SEGMENTATION_README.md        Full docs
│   └── SEGMENTATION_INDEX.md               This file
│
├── Core Scripts
│   ├── topic_segmentation.py               ⭐ Main script
│   ├── segment_locomo_batch.py             ⭐ Batch script
│   ├── analyze_segmentation.py             Analysis tool
│   └── test_segmentation.py                Test script
│
├── Config & Examples
│   ├── requirements_segmentation.txt       Dependencies
│   └── segmentation_example_output.json    Example output
│
└── Data Directories
    └── processed_data/
        ├── locomo_processed_data.json              Input
        ├── locomo_segmented_data.json              Output (main script)
        ├── locomo_segmented_test.json              Test output
        ├── locomo_segmented_batch/                 Batch outputs
        │   ├── locomo_conv-26_segmented.json
        │   ├── locomo_conv-30_segmented.json
        │   └── ...
        └── locomo_segmented_merged.json            Merged batch output
```

---

## 🎯 Usage Workflows

### Workflow 1: Quick Test & Run
**Files**: `test_segmentation.py` → `topic_segmentation.py` → `analyze_segmentation.py`

```bash
# 1. Test setup
python test_segmentation.py

# 2. Test with 2 conversations
python topic_segmentation.py --limit 2 --model gpt-4o-mini

# 3. Analyze results
python analyze_segmentation.py --validate

# 4. If OK, run full
python topic_segmentation.py --model gpt-4o-mini
```

### Workflow 2: Production Batch Processing
**Files**: `segment_locomo_batch.py` → `analyze_segmentation.py`

```bash
# 1. Process in batches
python segment_locomo_batch.py process --start 0 --end 5
python segment_locomo_batch.py process --start 5

# 2. Merge results
python segment_locomo_batch.py merge

# 3. Validate
python analyze_segmentation.py \
    --input ./processed_data/locomo_segmented_merged.json \
    --validate

# 4. Export readable
python analyze_segmentation.py \
    --input ./processed_data/locomo_segmented_merged.json \
    --export ./analysis/segments_readable.txt
```

### Workflow 3: Parallel Processing
**Files**: `segment_locomo_batch.py` (multiple terminals)

```bash
# Terminal 1
python segment_locomo_batch.py process --start 0 --end 3

# Terminal 2
python segment_locomo_batch.py process --start 3 --end 6

# Terminal 3
python segment_locomo_batch.py process --start 6

# After all complete
python segment_locomo_batch.py merge
```

---

## 🔑 Key Features by File

| File | Segmentation | Analysis | Batch | Test | Docs |
|------|-------------|----------|-------|------|------|
| `topic_segmentation.py` | ✅ | ❌ | ❌ | ❌ | ❌ |
| `segment_locomo_batch.py` | ✅ | ❌ | ✅ | ❌ | ❌ |
| `analyze_segmentation.py` | ❌ | ✅ | ❌ | ❌ | ❌ |
| `test_segmentation.py` | ✅ | ❌ | ❌ | ✅ | ❌ |
| `QUICKSTART_SEGMENTATION.md` | ❌ | ❌ | ❌ | ❌ | ✅ |
| `TOPIC_SEGMENTATION_README.md` | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## 📖 Reading Order

### For First-Time Users:
1. `QUICKSTART_SEGMENTATION.md` - Get started quickly
2. `test_segmentation.py` - Run test
3. `topic_segmentation.py` - Try with `--limit 2`
4. `analyze_segmentation.py` - Check results
5. `TOPIC_SEGMENTATION_README.md` - Deep dive when needed

### For Production Use:
1. `TOPIC_SEGMENTATION_README.md` - Understand methodology
2. `segment_locomo_batch.py` - Use batch processing
3. `analyze_segmentation.py` - Validate quality

### For Debugging:
1. `test_segmentation.py` - Verify setup
2. `analyze_segmentation.py --validate` - Check issues
3. `segmentation_example_output.json` - Reference correct structure

---

## 🆘 Quick Help

**Problem**: Don't know where to start  
**Solution**: Read `QUICKSTART_SEGMENTATION.md`

**Problem**: Want to understand theory  
**Solution**: Read `TOPIC_SEGMENTATION_README.md`

**Problem**: Setup not working  
**Solution**: Run `python test_segmentation.py`

**Problem**: Results look wrong  
**Solution**: Run `python analyze_segmentation.py --validate`

**Problem**: Need example output  
**Solution**: See `segmentation_example_output.json`

**Problem**: Want batch processing  
**Solution**: Use `segment_locomo_batch.py process`

**Problem**: Need readable format  
**Solution**: Use `analyze_segmentation.py --export`

---

## 📊 File Size Reference

Approximate sizes after processing Locomo dataset (~10 conversations):

- Input: `locomo_processed_data.json` → ~1-2 MB
- Output: `locomo_segmented_data.json` → ~1.5-3 MB
- Batch dir: `locomo_segmented_batch/` → ~1.5-3 MB total
- Readable export: `segments_readable.txt` → ~500 KB - 1 MB

---

## 🎓 Learning Path

### Beginner:
1. Install dependencies: `requirements_segmentation.txt`
2. Read: `QUICKSTART_SEGMENTATION.md`
3. Run: `test_segmentation.py`
4. Try: `topic_segmentation.py --limit 2`

### Intermediate:
1. Read: `TOPIC_SEGMENTATION_README.md`
2. Run: Full segmentation with `topic_segmentation.py`
3. Analyze: Use `analyze_segmentation.py`
4. Review: `segmentation_example_output.json`

### Advanced:
1. Use: `segment_locomo_batch.py` for batch processing
2. Customize: Modify prompts in scripts
3. Optimize: Tune model/temperature parameters
4. Integrate: Build pipeline with other tools

---

## 🔄 Version History

**v1.0** (Current)
- Initial release
- Basic segmentation functionality
- Batch processing support
- Analysis and validation tools
- Complete documentation

---

**Last Updated**: November 2025  
**Maintainer**: hungpv

---

**Ready to start?**

```bash
# Step 1: Install
pip install -r requirements_segmentation.txt

# Step 2: Set API key
export OPENAI_API_KEY='your-key'

# Step 3: Test
python test_segmentation.py

# Step 4: Run
python topic_segmentation.py --limit 2
```

📖 **Next**: Read `QUICKSTART_SEGMENTATION.md` for detailed workflows!

