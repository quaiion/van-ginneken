
def RestoreKeyPoints(points):
    if len(points) < 1:
        return [points[0], points[0]]
    
    key_points = [points[0]]  # Всегда включаем первую точку
    prev_direction = None
    
    for i in range(1, len(points)):
        current = points[i]
        prev = points[i-1]
        
        # Проверка целочисленности координат
        if not all(isinstance(c, int) for p in [prev, current] for c in p):
            raise ValueError("Все координаты должны быть целыми числами")
        
        dx = current[0] - prev[0]
        dy = current[1] - prev[1]
        
        # Проверка на диагональное движение
        if dx != 0 and dy != 0:
            raise ValueError(f"Диагональное движение между {prev} и {current}")
        
        # Определение текущего направления
        current_direction = 'vertical' if dx == 0 else 'horizontal'
        
        # Если направление изменилось - добавляем предыдущую точку
        if prev_direction and current_direction != prev_direction:
            key_points.append(prev)
        
        prev_direction = current_direction
    
    # Всегда добавляем последнюю точку
    key_points.append(points[-1])
    
    return key_points
