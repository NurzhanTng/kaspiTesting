from operator import truediv

from PIL import Image
from pyzbar.pyzbar import decode
import cv2
import time

def make_photo():
    # Открыть доступ к веб-камере (индекс 0 указывает на первую камеру)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Не удалось получить доступ к веб-камере.")
    else:
        # Захватить один кадр
        ret, frame = cap.read()

        if ret:
            # Сохранить кадр в файл
            cv2.imwrite("data/qr.jpg", frame)
            print("Фото сохранено как 'photo_from_webcam.jpg'.")
        else:
            print("Не удалось сделать фото.")

    # Освободить веб-камеру
    cap.release()

    # Закрыть все окна
    cv2.destroyAllWindows()

    # Загрузка изображения (можно использовать cv2 или Pillow)
    image_path = 'data/qr.jpg'
    image = Image.open(image_path)

    # Распознавание QR-кода
    qr_codes = decode(image)

    return qr_codes


if __name__ == '__main__':
    while True:
        # рест запрос на новую оплату с бека
        payment = True
        price = 1
        orderId = 1
        if payment:
            # рест запрос на новую оплату в каспи с price
            done = False
            while not done:
                qr_codes = make_photo()

                # Вывод информации о QR-кодах
                for qr in qr_codes:
                    done = True
                    print(qr)
                    qr_data = qr.data.decode('utf-8')
                    print(f'QR Data: {qr_data}')

                    # рест запрос на сохранение оплаты
        time.sleep(1)
