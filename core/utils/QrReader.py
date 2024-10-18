import logging
from PIL import Image
from pyzbar.pyzbar import decode
from typing import List, Tuple
import cv2


class QrReader:
    def __init__(self, camera_id=0, photo_path="data/qr.jpg"):
        self.camera_id = camera_id
        self.photo_path = photo_path
        self.cap = cv2.VideoCapture(camera_id)

    def close_camera(self):
        """Закрываем доступ к веб-камере"""
        self.cap.release()
        cv2.destroyAllWindows()

    def open_camera(self):
        """Открываем доступ к веб-камере"""
        self.cap = cv2.VideoCapture(self.camera_id)

    def make_photo(self) -> Tuple[List[str], str]:
        """Снимаем фото с камеры и возвращаем декодированные QR-коды"""
        if not self.cap.isOpened():
            logging.error("Не удалось получить доступ к веб-камере.")
            return [], "CapError"

        # Захватываем кадр с веб-камеры
        ret, frame = self.cap.read()

        if ret:
            # Сохраняем фото
            cv2.imwrite(self.photo_path, frame)

            # Загружаем фото и декодируем QR-коды
            image = Image.open(self.photo_path)
            qr_codes = decode(image)

            # Возвращаем декодированные данные из QR-кодов
            return [qr.data.decode('utf-8') for qr in qr_codes], "Success"
        else:
            logging.error("Не удалось сделать фото.")
            return [], "PhotoError"
