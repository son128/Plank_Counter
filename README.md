# UIT - IT001 - Đỗ Thanh Sơn - MSSV: 26521770
# Plank Counter
Ứng dụng đếm thời gian plank theo thời gian thực bằng camera, sử dụng MediaPipe Pose.
## Video demo
[Xem video demo](https://drive.google.com/file/d/1sUKob4FV3nuqfDIH_UKUTNtJVmKg97sF/view?usp=sharing)

## Ý tưởng
Người dùng nằm vào tư thế plank trước camera đặt ở bên hông. Chương trình kiểm tra
tư thế có đúng hay không và đếm số giây giữ tư thế, đồng thời lưu thời gian dài nhất.

## Cách hoạt động
Camera -> MediaPipe Pose -> Toạ độ vai, hông, mắt cá -> Góc hông + độ nghiêng thân -> Máy trạng thái đếm giờ -> Hiển thị

1. Input: 
    khung hình từ webcam.
2. MediaPipe Pose: 
    trả về 33 điểm mốc. Chương trình dùng vai, hông, mắt cá chân và chọn bên cơ thể có visibility cao hơn.
3. Thuật toán:
    Góc hông (vai - hông - mắt cá) tính bằng tích vô hướng: thân thẳng khi góc lớn hơn 150°.
    Độ nghiêng của đường vai - mắt cá so với phương ngang: thân nằm ngang khi nhỏ hơn 10°.
    Đúng tư thế khi thoả cả hai điều kiện.
4. Bộ đếm giờ: 
    đúng tư thế liên tục 1 giây thì bắt đầu đếm, sai tư thế liên tục 1 giây thì dừng và cập nhật Best. Sai ngắn hơn 1 giây thì được bỏ qua.
5. Output: số giây hiện tại và kỷ lục hiển thị trên màn hình.

## Yêu cầu
Windows, có webcam

Python 3.12

## Cài đặt
Chạy trong PowerShell, tại thư mục project lần lượt chạy các lệnh:

    py -3.12 -m venv venv

    .\venv\Scripts\Activate.ps1

    python -m pip install -r requirements.txt

Nếu PowerShell báo lỗi khi kích hoạt 'venv', chạy một lần:

    Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

## Chạy chương trình
Chạy trong PowerShell, tại thư mục project:

    python main.py

Bấm phím 'q' để thoát.

## Cách sử dụng
1. Đặt camera ở bên hông người tập sao cho thấy toàn thân từ vai đến mắt cá chân.
2. Vào tư thế plank và giữ yên khoảng 1 giây thì đồng hồ bắt đầu chạy.
3. Chữ màu xanh là đúng tư thế, màu đỏ là sai tư thế.
4. Khi sai tư thế quá 1 giây, đồng hồ dừng và Best được cập nhật.

# Cấu trúc project
main.py: Vòng lặp camera và hiển thị.

pose_tracker.py: Làm việc với MediaPipe: nhận diện, vẽ, lấy toạ độ.

plank_logic.py: Tính góc, kiểm tra tư thế plank, bộ đếm giờ.

requirements.txt: Danh sách thư viện.

# Thư viện sử dụng
mediapipe 0.10.14

opencv-python

numpy