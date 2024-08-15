import cv2
import numpy
import pytesseract as ptc

ptc.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def readCam():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if not ret:
        print('não há cameras')
        return
    while True:

        # Converter para tons de cinza
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Aplicar filtro de limiarização (ajuste o valor de threshold conforme necessário)
        thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)[1]

        # Encontrar contornos
        contours, hierarchy = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filtrar contornos (ajuste os parâmetros conforme necessário)
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w > 50 and h > 20:
                # Isolar a região da placa
                plate = gray[y:y+h, x:x+w]

                # Aplicar OCR
                text = ptc.image_to_string(plate)

                # Exibir o texto
                print(text)

                # Desenhar um retângulo na placa
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Exibir o frame
        cv2.imshow('frame', frame)

        # Sair ao pressionar 'q'
        if cv2.waitKey(1) == ord('q'):
            break

    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    readCam()
