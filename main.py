import cv2
import time
import os
os.environ['GST_DEBUG'] = 'queue:5'

def create_rtsp_pipeline(rtsp_url):
    gst_str = (
        f'rtspsrc location="{rtsp_url}" latency=0 buffer-mode=auto ! '
        'queue max-size-buffers=300 !'
        'decodebin ! '
        'videoconvert ! '
        'video/x-raw,format=BGR ! '
        'appsink'
        # 'appsink max-buffers=1 drop=True sync=false async=false'
    )
    print(f"Pipeline: {gst_str}")
    return gst_str

def simulate_slow_process(frame):
    """Simula un proceso lento"""
    print("Iniciando proceso lento...")
    
    # Guardar tiempo inicial
    start_time = time.time()
    
    # Simular proceso pesado (5 segundos)
    time.sleep(20)
    
    # Calcular tiempo transcurrido
    elapsed_time = time.time() - start_time
    print(f"Proceso lento completado. Tiempo transcurrido: {elapsed_time:.2f} segundos")
    
    # Solo para visualización, convertir a gris durante el proceso lento
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def main():
    rtsp_url = "rtsp://demoia:Demo1234@190.131.206.126:554/cam/realmonitor?channel=10&subtype=0" # sin DVR send Buffer
    # rtsp_url = "rtsp://demoia:Demo1234@201.184.163.42/cam/realmonitor?channel=6&subtype=0" # con DVR send Buffer
    pipeline = create_rtsp_pipeline(rtsp_url)
    
    cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
    
    if not cap.isOpened():
        print("Error: Could not open RTSP stream.")
        return
    
    # Variables para control de FPS y proceso lento
    frame_count = 0
    start_time = time.time()
    is_processing = False
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("Error reading frame.")
                break
            
            # Incrementar contador de frames
            frame_count += 1
            
            # Calcular y mostrar FPS cada 30 frames
            if frame_count % 30 == 0:
                elapsed_time = time.time() - start_time
                fps = frame_count / elapsed_time
                print(f"FPS: {fps:.2f}")
            
            # Manejar entrada de teclado
            key = cv2.waitKey(1) & 0xFF
            
            # Si se presiona 's', iniciar proceso lento
            if key == ord('s'):
                is_processing = True
                processed_frame = simulate_slow_process(frame)
                cv2.imshow('RTSP Stream', processed_frame)
                is_processing = False
            # Si se presiona 'q', salir
            elif key == ord('q'):
                break
            # Si no hay proceso lento, mostrar frame normal
            elif not is_processing:
                cv2.imshow('RTSP Stream', frame)
            
    except KeyboardInterrupt:
        print("Stopped by user")
    
    finally:
        # Mostrar estadísticas finales
        total_time = time.time() - start_time
        average_fps = frame_count / total_time
        print("\nEstadísticas finales:")
        print(f"Tiempo total: {total_time:.2f} segundos")
        print(f"Frames totales: {frame_count}")
        print(f"FPS promedio: {average_fps:.2f}")
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()