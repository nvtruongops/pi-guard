import os
import glob

def compile_thesis():
    base_dir = r'D:\Work\Do-an\docs\thesis'
    chapters_dir = os.path.join(base_dir, 'chapters')
    output_file = os.path.join(base_dir, 'FINAL_THESIS.md')
    
    chapter_files = sorted(glob.glob(os.path.join(chapters_dir, '*.md')))
    
    header_content = """# MINISTRY OF EDUCATION AND TRAINING
# FPT UNIVERSITY
## CAPSTONE PROJECT THESIS (IAP491)

# PI-GUARD: A MACHINE-LEARNING GUARDRAIL FOR DETECTING PROMPT INJECTION AND JAILBREAK ATTACKS ON LLM APPLICATIONS

**Academic Program**: Bachelor of Information Assurance (IA)  
**Capstone Code**: `IAP491_FA26_PI_GUARD`  
**Location & Year**: Hanoi, 2026  

---

### GROUP MEMBERS:
1. **Nguyễn Văn Trường (Leader)** — Student ID: `SE182034`
2. **Nguyễn Quí Đức** — Student ID: `SE182087`
3. **Phạm Minh Hoàng Việt** — Student ID: `SE181851`
4. **Đỗ Đoàn Duy Phương** — Student ID: `SE180235`

**Supervisor**: MSc. Supervisor / FPT University Department of Information Assurance  

---

"""
    
    compiled_parts = [header_content]
    
    for fpath in chapter_files:
        fname = os.path.basename(fpath)
        print(f'Adding: {fname}')
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            compiled_parts.append(content)
            compiled_parts.append('\n\n---\n\n')
            
    # Append References if available
    ref_file = r'D:\Work\Do-an\References\REFERENCES_LOG.md'
    if os.path.exists(ref_file):
        print('Appending References from REFERENCES_LOG.md')
        with open(ref_file, 'r', encoding='utf-8') as f:
            compiled_parts.append('# REFERENCES (TÀI LIỆU THAM KHẢO CHUẨN IEEE)\n\n')
            compiled_parts.append(f.read())
            
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(''.join(compiled_parts))
        
    print(f'Successfully compiled {len(chapter_files)} chapters into: {output_file}')

if __name__ == '__main__':
    compile_thesis()
