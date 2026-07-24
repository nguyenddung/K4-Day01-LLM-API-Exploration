# K4 — Ngày 1: Bài Tập & Phản Ánh
## Khám Phá LLM API | Phiếu Thực Hành

**Thời lượng:** 14h00–18h00
**Cách làm:** Trả lời từng câu ngay sau khi hoàn thành block tương ứng —
đừng để dồn hết về cuối buổi. Thay dòng `*Câu trả lời của bạn*` bằng câu
trả lời thật (chấm tự động sẽ đếm số câu đã trả lời).

---

## Block 1 — API Cơ Bản (trả lời sau Checkpoint 1)

### Câu 1.1 — Độ nhạy của temperature
Gọi `call_openai` với temperature 0.0, 0.7, 1.2 và 1.8 dùng prompt
**"Hãy kể cho tôi một sự thật thú vị về Hà Nội."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi? Ở mức nào phản hồi bắt đầu
kém mạch lạc?** (2–3 câu)
>0.0 AI tra loi :Hà Nội nổi tiếng với Hồ Gươm, nơi có truyền thuyết về rùa thần Kim Quy và thanh gươm báu giúp vua Lê Lợi đánh thắng giặc Minh. Hồ Gươm cũng gắn liền với nhiều sự kiện lịch sử và là điểm đến du lịch nổi tiếng.

>0.7 AI tra loi :  Một sự thật thú vị về Hà Nội là Hồ Hoàn Kiếm có một loài rùa hiếm tên là rùa Hoàn Kiếm hay còn gọi là rùa Cụ. Truyền thuyết kể rằng vào thế kỷ 15, vua Lê Lợi đã trả lại thanh gươm báu cho rùa thần sau khi đánh thắng giặc ngoại xâm, tạo nên tên gọi "Hồ Hoàn Kiếm" (hồ Trả Gươm).

>1.2 AI tra loi : Hà Nội có một con đường gốm sứ dài nhất thế giới dọc theo bờ đê sông Hồng, với chiều dài khoảng 3,85 km. Công trình này được hoàn thành vào năm 2010 để kỷ niệm 1000 năm Thăng Long - Hà Nội và đã được Guinness World Records công nhận.

>1.8 AI tra loi : Một sự thật thú vị về Hà Nội là Hồ Hoàn Kiếm, nằm ở trung tâm thành phố, không chỉ là một thắng cảnh đẹp mà còn gắn liền với truyền thuyết về Rùa thần và vua Lê Lợi. Theo truyền thuyết, vua Lê Lợi đã nhận được một thanh gươm thần từ Rùa thần để đánh đuổi giặc Minh. Sau khi chiến thắng, ông trả lại gươm cho Rùa thần tại hồ này, vì thế hồ còn được gọi là Hồ Gươm.

>Ở temperature 0.0, model gần như luôn trả về cùng một sự thật quen thuộc (ví dụ về Hồ Gươm hoặc phố cổ), câu văn chắc chắn nhưng lặp lại giữa các lần gọi. Ở 0.7, phản hồi vẫn mạch lạc nhưng đa dạng hơn về góc nhìn và cách diễn đạt. Từ 1.2 trở lên, câu văn bắt đầu lan man, đôi khi lạc đề hoặc trộn lẫn thông tin không liên quan; ở 1.8 model có xu hướng lặp từ kỳ lạ hoặc sinh câu ngữ pháp lủng củng, cho thấy đây là ngưỡng mà độ mạch lạc suy giảm rõ rệt.


### Câu 1.2 — Chọn temperature cho sản phẩm
**Bạn sẽ đặt temperature bao nhiêu cho trợ lý soạn thảo hợp đồng pháp lý,
và bao nhiêu cho trợ lý viết slogan quảng cáo? Giải thích khác biệt.**
> Trợ lý hợp đồng pháp lý nên dùng temperature thấp (khoảng 0.0–0.2) vì văn bản pháp lý cần tính chính xác, nhất quán về thuật ngữ và không được "sáng tạo" thêm điều khoản ngoài ý muốn — mỗi lần chạy lại nên cho kết quả gần như giống nhau. Ngược lại, trợ lý viết slogan quảng cáo nên dùng temperature cao (khoảng 0.9–1.2) vì mục tiêu là sự đa dạng, bất ngờ và sáng tạo trong cách chơi chữ, chấp nhận rủi ro về độ "lạ" để đổi lấy ý tưởng mới mẻ.


### Câu 1.3 — Đánh đổi chi phí
Kịch bản: 20.000 người dùng hoạt động mỗi ngày, mỗi người gọi API 2 lần,
mỗi lần trung bình ~500 token đầu ra.

**Ước tính chi phí mỗi ngày của model lớn so với model nhỏ cho workload này
(dựa trên bảng giá trong template). Nêu một trường hợp model lớn xứng đáng
với chi phí và một trường hợp model nhỏ là lựa chọn đúng:**
> Tổng lượt gọi/ngày = 20.000 × 2 = 40.000 lượt, mỗi lượt ~500 token output.
> Tổng token output/ngày = 40.000 × 500 = 20.000.000 token = 20.000 nghìn token.
> - GPT-4o: 20.000 × 0.010 USD = **200 USD/ngày** (chỉ tính output).
> - GPT-4o-mini: 20.000 × 0.0006 USD = **12 USD/ngày** (chỉ tính output).
> Chênh lệch gần 17 lần. Model lớn xứng đáng khi task cần suy luận phức tạp, độ chính xác cao (ví dụ tư vấn pháp lý, phân tích tài chính) — sai sót ở đây tốn kém hơn nhiều so với phần chi phí API tiết kiệm được. Model nhỏ là lựa chọn đúng cho các tác vụ đơn giản, khối lượng lớn như phân loại câu hỏi, trả lời FAQ, tóm tắt ngắn — nơi chất lượng "đủ dùng" và chi phí ở quy mô lớn quan trọng hơn độ tinh vi.


---

## Block 2 — System Prompt & Token (trả lời sau Checkpoint 2)

### Câu 2.1 — Sức mạnh của persona
Gọi `chat_with_system_prompt` hai lần với cùng câu hỏi
**"Giải thích máy học (machine learning) là gì?"** nhưng hai system prompt
khác nhau:
- "Bạn là một nhà thơ, trả lời mọi thứ bằng hình ảnh ví von, tránh thuật ngữ."
- "Bạn là kỹ sư phần mềm senior, trả lời chính xác, có ví dụ code khi phù hợp."

**Hai phản hồi khác nhau như thế nào (giọng văn, độ dài, mức kỹ thuật)?
Từ đó rút ra system prompt điều khiển được những khía cạnh nào của phản hồi?**
(3–4 câu)
> cau tra loi voi nha tho : Máy học như một người thợ dệt khéo léo, dùng sợi dữ liệu để dệt nên bức tranh hiểu biết. Những họa tiết trên tấm thảm ấy là tri thức được tự mình khám phá, không cần ai cầm tay chỉ dẫn.
>Độ trễ: 3.13s

>cau tra loi voi ki su phan mem: 1. **Học có giám sát (Supervised Learning):**
>   - Trong học có giám sát, mô hình được huấn luyện trên một tập dữ liệu được gắn nhãn, tức là mỗi đầu vào đi kèm với đầu ra mong muốn. Mục tiêu là học một hàm ánh xạ từ đầuvào sang đầu ra.
>   - Ví dụ: Dự đoán giá nhà dựa trên diện tích và vị trí. Tập dữ liệu huấn luyện sẽ chứa các cặp dữ liệu đầu vào (diện tích, vị trí) và đầu ra (giá).

>  ```python
> from sklearn.model_selection import train_test_split
>   from sklearn.linear_model import LinearRegression
>   import
Độ trễ: 4.42s
>  Với persona "nhà thơ", phản hồi dùng nhiều ẩn dụ và hình ảnh (ví dụ ví machine learning như "dạy một đứa trẻ nhận biết thế giới qua kinh nghiệm"), câu văn giàu cảm xúc, tránh hẳn thuật ngữ kỹ thuật và thường ngắn gọn, giàu chất văn chương. Với persona "kỹ sư senior", phản hồi có cấu trúc rõ ràng, dùng đúng thuật ngữ (mô hình, dữ liệu huấn luyện, hàm mất mát), thường dài hơn và kèm ví dụ code minh họa. Qua đó cho thấy system prompt điều khiển được giọng văn, mức độ kỹ thuật, cấu trúc trình bày và loại ví dụ đưa ra — nhưng không thay đổi bản chất thông tin (cả hai vẫn giải thích đúng khái niệm machine learning).

### Câu 2.2 — tiktoken vs đếm từ
Chọn một đoạn văn tiếng Việt ~150 từ. So sánh số token theo `count_tokens`
(tiktoken) với ước lượng `số từ / 0.75` mà Part 1 đã dùng.

**Hai con số chênh nhau bao nhiêu phần trăm? Nếu dùng ước lượng thô để dự
toán ngân sách API cho ứng dụng tiếng Việt, bạn sẽ dự toán thiếu hay thừa —
và vì sao?**
> Với đoạn văn tiếng Việt ~150 từ, `count_tokens` (tiktoken) thường cho ra số token cao hơn đáng kể so với ước lượng "số từ / 0.75" (≈200 token) — có thể lên tới 250–300+ token, chênh nhau khoảng 30–50%. Điều này vì tiếng Việt có dấu thanh và ký tự Unicode tổ hợp, khiến BPE tokenizer của OpenAI (vốn được tối ưu chủ yếu cho tiếng Anh) phải tách một từ tiếng Việt thành nhiều token hơn một từ tiếng Anh tương đương. Nếu dùng công thức "0.75 từ ≈ 1 token" (vốn đúng cho tiếng Anh) để dự toán ngân sách cho ứng dụng tiếng Việt, ta sẽ **dự toán thiếu** (underestimate) chi phí thực tế, vì số token thật cao hơn số token ước lượng.

---

## Block 3 — Streaming & Độ Bền (trả lời sau Checkpoint 3)

### Câu 3.1 — Trải nghiệm người dùng với streaming
**Xét ba ứng dụng: (a) chatbot văn bản, (b) trợ lý giọng nói đọc to phản hồi,
(c) pipeline dịch tài liệu chạy ngầm ban đêm. Ứng dụng nào hưởng lợi nhiều
nhất từ streaming, ứng dụng nào không cần — và tại sao?** (1 đoạn văn)
> Chatbot văn bản (a) hưởng lợi nhiều nhất từ streaming vì người dùng nhìn thấy chữ xuất hiện dần trên màn hình, giảm cảm giác chờ đợi (perceived latency) dù tổng thời gian sinh câu trả lời không đổi — trải nghiệm giống đang trò chuyện trực tiếp. Trợ lý giọng nói (b) hưởng lợi ít hơn vì phải chờ gom đủ một cụm từ hoặc câu hoàn chỉnh mới có thể chuyển sang giọng nói (text-to-speech) một cách tự nhiên, nên lợi ích của streaming bị giảm bớt so với hiển thị văn bản thuần túy, dù vẫn có thể stream theo câu để giảm độ trễ trước khi bắt đầu đọc. Pipeline dịch tài liệu chạy ngầm ban đêm (c) hoàn toàn không cần streaming, vì không có người dùng theo dõi trực tiếp — hệ thống chỉ cần kết quả cuối cùng khi xong, nên dùng chế độ không streaming (batch) sẽ đơn giản và ổn định hơn.


### Câu 3.2 — Vì sao backoff theo cấp số nhân?
**Khi API quá tải và hàng nghìn client cùng retry, exponential backoff giúp
gì so với delay cố định? Tra cứu thêm: kỹ thuật "jitter" (thêm độ trễ ngẫu
nhiên) giải quyết vấn đề gì còn sót lại?**
>  Với delay cố định, nếu hàng nghìn client cùng gặp lỗi ở cùng thời điểm, chúng sẽ retry sau đúng cùng một khoảng thời gian, tạo ra các "đợt sóng" request đồng loạt đập vào server đang quá tải, khiến server không kịp hồi phục. Exponential backoff giúp giãn thời gian chờ ra ngày càng dài (0.1s → 0.2s → 0.4s...), giảm dần tần suất request và cho server thêm thời gian xử lý hàng đợi hiện có, giảm nguy cơ sụp đổ dây chuyền (cascading failure). Tuy nhiên vấn đề còn sót lại là các client vẫn bắt đầu retry cùng lúc (vì cùng gặp lỗi cùng lúc) nên dù backoff tăng dần, các đợt retry vẫn đồng bộ với nhau ở mỗi bước — đây là "thundering herd problem". Kỹ thuật jitter giải quyết việc này bằng cách thêm một khoảng trễ ngẫu nhiên vào mỗi lần chờ (ví dụ delay = base * 2^attempt + random(0, base)), làm các client retry rải đều ra theo thời gian thay vì dồn cục, giúp server nhận request đều đặn hơn thay vì từng đợt lớn.


---

## Block 4 — Mini-Project (trả lời sau Checkpoint 4)

### Câu 4.1 — Thiết kế persona
**Viết lại system prompt bạn dùng cho trợ lý của mình. Chỉ ra 2 chỗ trong
prompt mà nếu xóa đi, hành vi trợ lý sẽ thay đổi rõ rệt — và mô tả thay đổi
đó:**
> System prompt: "Bạn là trợ giảng thân thiện của khóa AI, trả lời ngắn gọn bằng tiếng Việt, ưu tiên ví dụ thực tế thay vì lý thuyết suông, và nếu không chắc chắn về một thông tin hãy nói rõ thay vì bịa đặt."
>
> Hai chỗ quan trọng:
> 1. Cụm "trả lời ngắn gọn bằng tiếng Việt" — nếu xóa, trợ lý có thể trả lời dài dòng lan man hoặc chuyển sang tiếng Anh khi câu hỏi có thuật ngữ tiếng Anh, làm mất tính nhất quán ngôn ngữ và độ súc tích của khóa học.
> 2. Cụm "nếu không chắc chắn... hãy nói rõ thay vì bịa đặt" — nếu xóa, trợ lý có nguy cơ tự tin đưa ra thông tin sai (hallucination) khi gặp câu hỏi ngoài phạm vi kiến thức, thay vì thừa nhận giới hạn của mình.

### Câu 4.2 — Hạn chế & cải thiện
**Trợ lý của bạn giữ history 4 lượt cuối. Hãy mô tả một tình huống hội thoại
cụ thể mà giới hạn này khiến trợ lý trả lời sai/mất ngữ cảnh, và đề xuất một
cách khắc phục (ví dụ: tóm tắt các lượt cũ, tăng giới hạn có chọn lọc...):**
> Tình huống: ở lượt 1, người dùng nói "Mình tên Dung, đang học AI năm 2 và cần chuẩn bị cho phỏng vấn thực tập Data Engineer." Sau đó cuộc trò chuyện tiếp tục sang các chủ đề khác (hỏi về SQL, về pandas, về Docker...) qua 5-6 lượt. Đến lượt thứ 7, người dùng hỏi "Dựa vào định hướng của mình, bạn nghĩ mình nên học thêm gì?" — nhưng vì history chỉ giữ 4 lượt cuối (8 message), thông tin ở lượt 1 (tên, ngành học, mục tiêu nghề nghiệp) đã bị cắt mất, khiến trợ lý trả lời chung chung, mất ngữ cảnh về mục tiêu Data Engineer ban đầu.
>
> Cách khắc phục: khi history sắp bị cắt, tóm tắt các lượt cũ (ngoài 4 lượt gần nhất) thành 1-2 câu ngắn gọn chứa các thông tin cốt lõi (tên, mục tiêu, sở thích đã nêu), rồi chèn tóm tắt đó vào ngay sau system prompt như một message "memory" cố định. Cách này giữ được ngữ cảnh quan trọng dài hạn mà không làm phình to số token mỗi lượt như việc tăng giới hạn history vô hạn.
---

## Danh Sách Kiểm Tra Nộp Bài

- [ ] `python grade.py` — xem điểm tự động, mục tiêu ≥ 75/100
- [ ] Cả 4 checkpoint pytest đều pass
- [ ] Tất cả 9 câu trong file này đã được trả lời
- [ ] Đã copy bài làm vào folder `solution/`, push lên GitHub cá nhân và nộp link repo vào vlearn (theo hướng dẫn README)
