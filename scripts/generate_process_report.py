import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

def generate_report():
    wb = openpyxl.Workbook()
    
    # ==========================================
    # SHEET 1: PROCESS REPORT (CHUẨN FPT EXCEL)
    # ==========================================
    ws = wb.active
    ws.title = '1. Báo Cáo Tiến Độ'
    ws.views.sheetView[0].showGridLines = True


    # Styles & Colors
    navy_header_fill = PatternFill(start_color='1F497D', end_color='1F497D', fill_type='solid')
    blue_sub_fill = PatternFill(start_color='DCE6F1', end_color='DCE6F1', fill_type='solid')
    zebra_fill = PatternFill(start_color='F9FAFB', end_color='F9FAFB', fill_type='solid')

    white_bold_font = Font(name='Calibri', size=11, bold=True, color='FFFFFF')
    title_font = Font(name='Calibri', size=15, bold=True, color='1F497D')
    subtitle_font = Font(name='Calibri', size=10, bold=True, color='366092')
    bold_font = Font(name='Calibri', size=10, bold=True)
    regular_font = Font(name='Calibri', size=10)

    thin_border = Border(
        left=Side(style='thin', color='B0C4DE'),
        right=Side(style='thin', color='B0C4DE'),
        top=Side(style='thin', color='B0C4DE'),
        bottom=Side(style='thin', color='B0C4DE')
    )

    # Title Block
    ws.merge_cells('A1:U1')
    ws['A1'] = 'BÁO CÁO TIẾN ĐỘ THỰC HIỆN ĐỒ ÁN TỐT NGHIỆP (CAPSTONE PROCESS REPORT)'
    ws['A1'].font = title_font
    ws['A1'].alignment = Alignment(horizontal='center', vertical='center')

    ws.merge_cells('A2:U2')
    ws['A2'] = 'Code: IAP491_FA26_PI_GUARD | Supervisor: MSc. Supervisor / FPT University IA Department'
    ws['A2'].font = subtitle_font
    ws['A2'].alignment = Alignment(horizontal='center', vertical='center')

    ws.merge_cells('A3:U3')
    ws['A3'] = 'Topic: A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications (PI-Guard)'
    ws['A3'].font = Font(name='Calibri', size=10, italic=True, bold=True, color='1F497D')
    ws['A3'].alignment = Alignment(horizontal='center', vertical='center')

    # Headers Row 4 & 5
    ws.merge_cells('A4:A5')
    ws['A4'] = 'MSSV'
    ws.merge_cells('B4:B5')
    ws['B4'] = 'Họ và tên'

    ws.merge_cells('C4:F4')
    ws['C4'] = 'Phân công nhiệm vụ cốt lõi'
    ws['C5'] = 'Nhiệm vụ 1'
    ws['D5'] = 'Nhiệm vụ 2'
    ws['E5'] = 'Nhiệm vụ 3'
    ws['F5'] = 'Nhiệm vụ 4'

    ws.merge_cells('G4:U4')
    ws['G4'] = 'Tiến độ thực hiện hàng tuần (Tuần 1 - Tuần 15)'

    weeks = [f'Tuần {i}' for i in range(1, 16)]
    for idx, w in enumerate(weeks):
        col = get_column_letter(7 + idx)
        ws[f'{col}5'] = w

    for col_idx in range(1, 22):
        c1 = ws.cell(row=4, column=col_idx)
        c2 = ws.cell(row=5, column=col_idx)
        c1.fill = navy_header_fill
        c1.font = white_bold_font
        c1.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        c2.fill = blue_sub_fill
        c2.font = bold_font
        c2.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        c1.border = thin_border
        c2.border = thin_border

    # Member data
    members = [
        {
            'mssv': 'SE182034',
            'name': 'Nguyễn Văn Trường (Leader)',
            'nv1': 'Thiết kế kiến trúc hệ thống PI-Guard, thu thập và xây dựng Dataset đa nguồn (Hugging Face).',
            'nv2': 'Nghiên cứu & triển khai thuật toán Group-Aware Splitting chống rò rỉ dữ liệu (Data Leakage).',
            'nv3': 'Phụ trách Report No.1 (Introduction) & Report No.2 (Literature Review).',
            'nv4': 'Điều phối tiến độ nhóm, chuẩn hóa hồ sơ Review 1 - 4 và nộp báo cáo tuần cho GVHD.',
            'w1': 'Khởi động đồ án:\n- Đăng ký đề tài PI-Guard với GVHD.\n- Phân công nhiệm vụ 4 thành viên.\n- Thiết lập cấu trúc repo Git.',
            'w2': 'Khảo sát & Bối cảnh:\n- Khảo sát OWASP LLM01:2025 & NIST AI 100-2e2025.\n- Thu thập 17 papers tham khảo >= 2022.\n- Soạn thảo Background & Problem Statement.',
            'w3': 'Hoàn thành Review 1:\n- Hoàn thiện Report No.1 (Introduction).\n- Phân tích Threat Taxonomy.\n- Chuẩn bị slide PPT Review 1 và bảo vệ trước GVHD.',
            'w4': 'Báo cáo No.2 (Literature Review):\n- Khảo sát SOTA Guardrails (ProtectAI, Llama Guard, NeMo).\n- Viết Report No.2 nộp GVHD.'
        },
        {
            'mssv': 'SE182087',
            'name': 'Nguyễn Quí Đức',
            'nv1': 'Nghiên cứu lý thuyết Classical Machine Learning và biểu diễn đặc trưng ngôn ngữ.',
            'nv2': 'Xây dựng pipeline trích xuất đặc trưng kết hợp (Word + Char n-grams TF-IDF).',
            'nv3': 'Huấn luyện và đánh giá các mô hình Baseline (Logistic Regression, LinearSVC, XGBoost).',
            'nv4': 'Phụ trách Report No.3 (Methodology - Baseline ML & Feature Engineering).',
            'w1': 'Thiết lập môi trường ML:\n- Cài đặt Python 3.11, Scikit-learn, PyTorch.\n- Tìm hiểu cơ chế Word/Char TF-IDF.',
            'w2': 'Threat Model & Robustness:\n- Xây dựng sơ đồ Threat Model & Attack Surface.\n- Phân tích cơ chế kháng nhiễu Leetspeak/Base64.',
            'w3': 'Hoàn thành Review 1:\n- Chuẩn bị slide Threat Model & Kiến trúc 3 lớp.\n- Bắt đầu xây dựng baseline TF-IDF script.',
            'w4': 'Baseline Training:\n- Huấn luyện mô hình Logistic Regression, LinearSVC trên tập train.\n- Đánh giá F1 ban đầu.'
        },
        {
            'mssv': 'SE181851',
            'name': 'Phạm Minh Hoàng Việt',
            'nv1': 'Nghiên cứu cơ chế Disentangled Attention của mô hình microsoft/deberta-v3-base.',
            'nv2': 'Thực hiện Supervised Fine-Tuning Transformer và tối ưu hàm mất mát BCEWithLogitsLoss.',
            'nv3': 'Lượng hóa động ONNX INT8 Runtime để tối ưu độ trễ P95 < 30ms trên CPU.',
            'nv4': 'Phụ trách Report No.4 (Experimental and Results - Training & Adversarial Tests).',
            'w1': 'Khảo sát Transformer:\n- Tìm hiểu DeBERTa-v3 architecture.\n- Khảo sát mô hình tham chiếu ProtectAI DeBERTa.',
            'w2': 'Ma trận chọn mô hình:\n- Xây dựng Model Selection Matrix.\n- Thiết lập benchmark 5 Target LLM qua Cloud API (GPT-4o, Gemini, LLaMA-3.1).',
            'w3': 'Hoàn thành Review 1:\n- Xây dựng ma trận 4 Demo kịch bản (2x2).\n- Thử nghiệm đo độ trễ Latency trên CPU.',
            'w4': 'Fine-tuning Transformer:\n- Chuẩn bị pipeline huấn luyện DeBERTa-v3 trên GPU Colab/Kaggle.\n- Chạy baseline test.'
        },
        {
            'mssv': 'SE180235',
            'name': 'Đỗ Đoàn Duy Phương',
            'nv1': 'Phát triển Asynchronous API Middleware bằng FastAPI tích hợp chốt chặn Guardrail.',
            'nv2': 'Xây dựng giao diện Dashboard tương tác trực quan bằng Streamlit phục vụ kiểm thử.',
            'nv3': 'Định dạng và biên tập toàn văn Luận văn tốt nghiệp theo chuẩn FPT IAP491.',
            'nv4': 'Phụ trách Report No.5 (Discussion) & Report No.6 (Conclusion & Slide Deck).',
            'w1': 'Khảo sát hạ tầng API:\n- Thiết lập khung dự án FastAPI & Streamlit.\n- Thiết kế kiến trúc proxy chuyển tiếp LLM.',
            'w2': 'Research Questions & Scope:\n- Soạn thảo 3 Câu hỏi nghiên cứu cốt lõi chuẩn IEEE.\n- Phân định rõ ràng ranh giới In-scope / Out-of-scope.',
            'w3': 'Hoàn thành Review 1:\n- Thiết kế bộ slide 9 trang Review1_Presentation_Slides_Outline.md.\n- Dựng demo UI mô phỏng 4 kịch bản.',
            'w4': 'Phát triển API Middleware:\n- Hoàn thiện endpoint POST /v1/chat/guardrail.\n- Tích hợp mô hình baseline vào API.'
        }
    ]

    for row_idx, mem in enumerate(members, start=6):
        ws.cell(row=row_idx, column=1, value=mem['mssv'])
        ws.cell(row=row_idx, column=2, value=mem['name'])
        ws.cell(row=row_idx, column=3, value=mem['nv1'])
        ws.cell(row=row_idx, column=4, value=mem['nv2'])
        ws.cell(row=row_idx, column=5, value=mem['nv3'])
        ws.cell(row=row_idx, column=6, value=mem['nv4'])
        ws.cell(row=row_idx, column=7, value=mem.get('w1', ''))
        ws.cell(row=row_idx, column=8, value=mem.get('w2', ''))
        ws.cell(row=row_idx, column=9, value=mem.get('w3', ''))
        ws.cell(row=row_idx, column=10, value=mem.get('w4', ''))
        
        for c in range(11, 22):
            ws.cell(row=row_idx, column=c, value='[ ] Kế hoạch theo lộ trình')

        for c in range(1, 22):
            cell = ws.cell(row=row_idx, column=c)
            cell.font = regular_font
            cell.border = thin_border
            cell.alignment = Alignment(vertical='top', wrap_text=True)
            if row_idx % 2 == 1:
                cell.fill = zebra_fill

    # ==========================================
    # SHEET 2: INTERACTIVE CHECKLIST
    # ==========================================
    ws_check = wb.create_sheet(title='2. Checklist Tiến Độ')
    ws_check.views.sheetView[0].showGridLines = True


    ws_check.merge_cells('A1:G1')
    ws_check['A1'] = 'DANH MỤC CÔNG VIỆC CHI TIẾT & CHECKLIST TIẾN ĐỘ (PI-GUARD CAPSTONE)'
    ws_check['A1'].font = title_font
    ws_check['A1'].alignment = Alignment(horizontal='center', vertical='center')

    ws_check.merge_cells('A2:G2')
    ws_check['A2'] = 'Hướng dẫn: Chọn trạng thái tại cột D từ danh sách thả xuống (Dropdown List)'
    ws_check['A2'].font = subtitle_font
    ws_check['A2'].alignment = Alignment(horizontal='center', vertical='center')

    check_headers = ['Mã Task', 'Tuần / Cột mốc', 'Nội dung công việc', 'Trạng thái', 'Thành viên phụ trách', 'Sản phẩm đầu ra', 'Ghi chú / Deadline']
    for col_idx, h in enumerate(check_headers, start=1):
        c = ws_check.cell(row=4, column=col_idx, value=h)
        c.fill = navy_header_fill
        c.font = white_bold_font
        c.alignment = Alignment(horizontal='center', vertical='center')
        c.border = thin_border

    # Data validation dropdown for Status
    dv = DataValidation(type='list', formula1='"Hoàn thành,Đang thực hiện,Chưa bắt đầu"', allow_blank=True)
    ws_check.add_data_validation(dv)
    dv.add('D5:D50')

    tasks = [
        ('T01', 'Tuần 1 (23/08 - 29/08)', 'Họp với Giáo viên hướng dẫn (GVHD) và xác định mục tiêu ban đầu (Meeting 1)', 'Hoàn thành', 'Trường (Leader)', 'Biên bản Meeting 1_29_08_26.md', '29/08/2026'),
        ('T02', 'Tuần 1 (23/08 - 29/08)', 'Khảo sát tài liệu nghiên cứu và thu thập 17 papers chuẩn IEEE >= 2022', 'Đang thực hiện', 'Trường', 'References/ & REFERENCES_LOG.md', '30/08/2026'),
        ('T03', 'Tuần 2 (30/08 - 05/09)', 'Soạn thảo Chapter 1: Background & Problem Statement (Lỗ hổng Von Neumann NLP)', 'Đang thực hiện', 'Trường', 'workspaces/truong_data_eng/docs/', '31/08/2026'),
        ('T04', 'Tuần 2 (30/08 - 05/09)', 'Phân loại Threat Taxonomy (Direct/Indirect Injection vs Jailbreak theo OWASP)', 'Đang thực hiện', 'Trường & Đức', 'workspaces/truong_data_eng/docs/', '31/08/2026'),
        ('T05', 'Tuần 2 (30/08 - 05/09)', 'Xây dựng Threat Model (NIST AI 100-2e2025) & Attack Surface (/v1/chat)', 'Đang thực hiện', 'Đức', 'workspaces/duc_baseline_ml/', '01/09/2026'),
        ('T06', 'Tuần 2 (30/08 - 05/09)', 'Thiết kế Kiến trúc bảo vệ 3 lớp & Cơ chế phòng thủ độ bền Robustness', 'Đang thực hiện', 'Đức', 'workspaces/duc_baseline_ml/', '02/09/2026'),
        ('T07', 'Tuần 2 (30/08 - 05/09)', 'Soạn thảo 3 Câu hỏi nghiên cứu IEEE (RQ1-RQ3), 3 Gaps & 4 Đóng góp mới', 'Đang thực hiện', 'Phương', 'workspaces/phuong_api_dashboard/', '01/09/2026'),
        ('T08', 'Tuần 2 (30/08 - 05/09)', 'Khảo sát SOTA Guardrails, Model Selection Matrix & Benchmark 5 Target LLMs', 'Đang thực hiện', 'Việt', 'workspaces/viet_transformer_robustness/', '02/09/2026'),
        ('T09', 'Tuần 2 (30/08 - 05/09)', 'Thiết kế & kiểm thử Ma trận 4 Kịch bản Demo (2x2: Vulnerable vs Protected)', 'Đang thực hiện', 'Việt & Phương', 'workspaces/viet_transformer_robustness/', '03/09/2026'),
        ('T10', 'Tuần 2 (30/08 - 05/09)', 'Hoàn thiện toàn văn Report No.1: Introduction (Chapter 1 — 10% Process Mark)', 'Đang thực hiện', 'Trường (Leader)', 'workspaces/truong_data_eng/docs/', '04/09/2026'),
        ('T11', 'Tuần 2 (30/08 - 05/09)', 'Hoàn thiện toàn văn Report No.2: Literature Review (Chapter 2 — 25% Process Mark)', 'Đang thực hiện', 'Trường & Phương', 'workspaces/truong_data_eng/docs/', '04/09/2026'),
        ('T12', 'Tuần 2 (30/08 - 05/09)', 'Thiết kế dàn ý slide 9 trang Review 1 Presentation Slides (Bao gồm 2 Chương)', 'Đang thực hiện', 'Phương', 'workspaces/truong_data_eng/docs/', '04/09/2026'),
        ('T13', 'Tuần 2 (30/08 - 05/09)', 'Thiết kế slide PowerPoint (.pptx) & Tập dượt thuyết trình 15 phút (2 Chương)', 'Chưa bắt đầu', 'Cả 4 thành viên', 'Slide PPTX Review 1', '05/09/2026'),
        ('T14', 'Tuần 2 (30/08 - 05/09)', 'Họp tổng kết tuần, cập nhật Process Report Excel & Nộp Report 1 & 2 cho GVHD', 'Chưa bắt đầu', 'Trường (Leader)', 'PI_GUARD_PROCESS_REPORT.xlsx', '06/09/2026'),
        ('T15', 'Tuần 3 - 4 (06/09 - 19/09)', 'CỘT MỐC 1 — BẢO VỆ REVIEW 1 TRƯỚC GVHD (CHAPTERS 1 & 2)', 'Chưa bắt đầu', 'Cả 4 thành viên', 'Biên bản nghiệm thu Review 1', 'Tuần 3-4'),
        ('T16', 'Tuần 5 - 6 (20/09 - 03/10)', 'Thu thập Dataset, Group-Aware Split & Huấn luyện Baseline ML', 'Chưa bắt đầu', 'Trường & Đức', 'data/processed/ & models/baseline/', 'Tuần 6'),
        ('T17', 'Tuần 7 (04/10 - 10/10)', 'CỘT MỐC 2 — Nộp Report No.3 & BẢO VỆ REVIEW 2 TRƯỚC GVHD (CHAPTER 3)', 'Chưa bắt đầu', 'Đức & Trường', 'Report No.3 & Demo Baseline', 'Tuần 7'),
        ('T18', 'Tuần 8 - 9 (11/10 - 24/10)', 'Fine-tuning DeBERTa-v3, Lượng hóa ONNX INT8 & Nộp Report No.4', 'Chưa bắt đầu', 'Việt & Đức', 'Report No.4 & models/onnx/', 'Tuần 9'),
        ('T19', 'Tuần 10 - 12 (25/10 - 14/11)', 'CỘT MỐC 3 — BÁO CÁO HỘI ĐỒNG 1 (HỘI ĐỒNG GIỮA KỲ — PROTOTYPE DEMO)', 'Chưa bắt đầu', 'Phương & Việt', 'Hệ thống Prototype hoàn chỉnh', 'Tuần 12'),
        ('T20', 'Tuần 13 - 15 (15/11 - 05/12)', 'CỘT MỐC 4 — BÁO CÁO HỘI ĐỒNG FINAL (BẢO VỆ TỐT NGHIỆP TOÀN DIỆN 6 CHƯƠNG)', 'Chưa bắt đầu', 'Cả 4 thành viên', 'Final Thesis & Slide Defense', 'Tuần 15')
    ]

    for row_idx, task in enumerate(tasks, start=5):
        for col_idx, val in enumerate(task, start=1):
            c = ws_check.cell(row=row_idx, column=col_idx, value=val)
            c.font = regular_font
            c.border = thin_border
            if col_idx == 4:
                c.alignment = Alignment(horizontal='center', vertical='center')
                if val == 'Hoàn thành':
                    c.fill = PatternFill(start_color='E2EFDA', end_color='E2EFDA', fill_type='solid')
                    c.font = Font(name='Calibri', size=10, bold=True, color='375623')
                elif val == 'Đang thực hiện':
                    c.fill = PatternFill(start_color='FFF2CC', end_color='FFF2CC', fill_type='solid')
                    c.font = Font(name='Calibri', size=10, bold=True, color='7F6000')
                else:
                    c.fill = zebra_fill
            elif col_idx in [1, 2, 7]:
                c.alignment = Alignment(horizontal='center', vertical='center')
            else:
                c.alignment = Alignment(vertical='center', wrap_text=True)

    # Column dimensions
    ws.column_dimensions['A'].width = 12
    ws.column_dimensions['B'].width = 25
    ws.column_dimensions['C'].width = 30
    ws.column_dimensions['D'].width = 30
    ws.column_dimensions['E'].width = 30
    ws.column_dimensions['F'].width = 30
    for col_idx in range(7, 22):
        ws.column_dimensions[get_column_letter(col_idx)].width = 35

    ws_check.column_dimensions['A'].width = 10
    ws_check.column_dimensions['B'].width = 24
    ws_check.column_dimensions['C'].width = 45
    ws_check.column_dimensions['D'].width = 20
    ws_check.column_dimensions['E'].width = 18
    ws_check.column_dimensions['F'].width = 32
    ws_check.column_dimensions['G'].width = 15

    # Row heights
    ws.row_dimensions[1].height = 25
    ws.row_dimensions[2].height = 20
    ws.row_dimensions[3].height = 20
    ws.row_dimensions[4].height = 25
    ws.row_dimensions[5].height = 25
    for r in range(6, 10):
        ws.row_dimensions[r].height = 90

    ws_check.row_dimensions[1].height = 25
    ws_check.row_dimensions[2].height = 20
    ws_check.row_dimensions[4].height = 25
    for r in range(5, len(tasks) + 5):
        ws_check.row_dimensions[r].height = 25

    # Save outputs
    out_paths = [
        r'D:\Work\Do-an\Meeting\PI_GUARD_PROCESS_REPORT.xlsx',
        r'D:\Work\Do-an\reports\PI_GUARD_PROCESS_REPORT.xlsx'
    ]
    for p in out_paths:
        wb.save(p)
        print(f'Saved: {p}')

if __name__ == '__main__':
    generate_report()
