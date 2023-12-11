import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class EggTimerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("간편 요리 타이머!")

        self.remaining_time = 8 * 60  # 초 단위로 설정 (8분)
        self.timer_running = False

        # 간편요리타이머 레이블
        self.title_label = tk.Label(self.master, text="간편 요리 타이머", font=("Helvetica", 30, "bold"))
        self.title_label.pack(pady=20)
        self.label = tk.Label(self.master, text="", font=("Helvetica", 80))
        self.label.pack(pady=10)
        self.label.place(x=200, y=500)  # 레이블 위치 설정

        # 타이머 레이블
        self.label = tk.Label(self.master, text="", font=("Helvetica", 80))
        self.label.pack(pady=10)
        self.label.place(x=200, y=200)  # 레이블 위치 설정

        self.start_button = tk.Button(self.master, text="반숙 계란 타이머", command=self.start_timer, bg="yellow", fg="black", width=20, height=3)
        self.start_button.place(x=80, y=400)  # 첫 번째 버튼 위치 설정

        self.second_button = tk.Button(self.master, text="완숙 계란 타이머", command=self.start_12min_timer, bg="yellow", fg="black", width=20, height=3)
        self.second_button.place(x=308, y=400)  # 두 번째 버튼 위치 설정

        self.create_additional_buttons()  # 세 개의 추가 버튼 생성

        self.stop_timer_button = None  # 초기에는 버튼을 생성하지 않음

        # 이미지를 표시할 레이블
        self.image_label = tk.Label(self.master)
        self.image_label.pack(pady=10)
        self.image_label.place(x=250, y=80)  # 이미지 레이블 위치 설정

    def format_time(self):
        minutes, seconds = divmod(self.remaining_time, 60)
        return f"{minutes:02d}:{seconds:02d}"

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.create_stop_timer_button()  # 타이머 시작 후에 버튼 생성
            self.update_label()

            # '반숙 계란 타이머' 버튼을 눌렀을 때 이미지 표시 및 8분 뒤에 숨기기
            self.show_image("/Users/choijiyoung/project/images/반숙.png", width=100, height=100)
            self.master.after(8 * 60 * 1000, self.hide_image)

    def stop_timer(self):
        self.timer_running = False
        self.create_stop_timer_button()  # 타이머 정지 후에 버튼 생성
        self.remove_stop_timer_button()  # 타이머 정지 후에 버튼 제거

        # 타이머 정지 시 이미지 숨기기
        self.hide_image()

    def restart_timer(self):
        self.create_stop_timer_button()  # 타이머 재시작 후에 버튼 생성
        self.remove_stop_timer_button()  # 타이머 재시작 후에 버튼 제거
        self.start_timer()

    def create_stop_timer_button(self):
        if self.stop_timer_button is None:
            self.stop_timer_button = tk.Button(self.master, text="타이머 정지", command=self.stop_timer, bg="white", fg="red", width=10, height=2)
            self.stop_timer_button.place(x=245, y=330)  # 화면 정중앙에 배치
        else:
            self.stop_timer_button.config(text="타이머 재시작", command=self.restart_timer)

    def remove_stop_timer_button(self):
        if self.stop_timer_button is not None:
            self.stop_timer_button.destroy()
            self.stop_timer_button = None

    def update_label(self):
        if self.timer_running:
            self.remaining_time -= 1
            self.label.config(text=self.format_time())

            if self.remaining_time > 0:
                self.master.after(1000, self.update_label)
            else:
                self.timer_running = False
                self.create_stop_timer_button()  # 타이머 완료 후에 버튼 생성
                self.remove_stop_timer_button()  # 타이머 완료 후에 버튼 제거
                messagebox.showinfo("타이머 완료", "타이머가 완료되었습니다. 이제 맛있게 드세요!")

    def start_12min_timer(self):
        # 12분 타이머 시작
        self.remaining_time = 12 * 60
        self.start_timer()

        # '완숙 계란 타이머' 버튼을 눌렀을 때 이미지 표시 및 12분 뒤에 숨기기
        self.show_image("/Users/choijiyoung/project/images/완숙.png", width=100, height=100)
        self.master.after(12 * 60 * 1000, self.hide_image)

    def create_additional_buttons(self):
        # 세 개의 추가 버튼 생성
        button_data = [
            {"interval": 3 * 60, "text": "꼬들 라면 타이머", "image_path": "/Users/choijiyoung/project/images/꼬들라면.png"},
            {"interval": 4 * 60, "text": "보통 라면 타이머", "image_path": "/Users/choijiyoung/project/images/평범라면.png"},
            {"interval": 5 * 60, "text": "퍼진 라면 타이머", "image_path": "/Users/choijiyoung/project/images/부들라면.png"}
        ]

        for i, data in enumerate(button_data):
            button = tk.Button(self.master, text=data["text"], command=lambda interval=data["interval"], image_path=data["image_path"]: self.start_additional_timer(interval, image_path), bg="yellow", fg="black", width=12, height=3)
            button.place(x=80 + i * 150, y=480)  # 추가 버튼 위치 설정

    def start_additional_timer(self, interval, image_path):
        self.remaining_time = interval
        self.start_timer()

        # 버튼을 눌렀을 때 이미지 표시 및 지정된 시간 뒤에 숨기기
        self.show_image(image_path, width=100, height=100)
        self.master.after(interval * 1000, self.hide_image)

    def show_image(self, image_path, width=None, height=None):
        image = Image.open(image_path)
        if width and height:
            image = image.resize((width, height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo

    def hide_image(self):
        self.image_label.configure(image="")
        self.image_label.image = None

if __name__ == "__main__":
    root = tk.Tk()

    # 윈도우 크기를 600x600으로 설정
    root.geometry("600x600")


    app = EggTimerApp(root)
    root.mainloop()

