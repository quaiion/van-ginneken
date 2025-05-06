def GetPoints(start, end):
    """Генерирует точки между двумя точками на одной оси"""
    x1, y1 = start
    x2, y2 = end
    
    points = []
    
    # Вертикальная линия
    if x1 == x2:
        step = 1 if y2 > y1 else -1
        for y in range(y1, y2 + step, step):
            points.append([x1, y])
    
    # Горизонтальная линия
    elif y1 == y2:
        step = 1 if x2 > x1 else -1
        for x in range(x1, x2 + step, step):
            points.append([x, y1])
    
    else:
        raise ValueError("Точки должны быть на одной оси")
    
    return points

def GetFullPath(segments):
    """Генерирует все точки ломаной линии"""
    if not segments:
        return []
    
    path = []
    
    for i in range(len(segments) - 1):
        start = segments[i]
        end = segments[i+1]
        
        segment_points = GetPoints(start, end)
        
        # Удаляем дубликат точки соединения между сегментами
        if i > 0:
            segment_points = segment_points[1:]
            
        path.extend(segment_points)
    
    if len(path) == 1:
        path.append(path[0])

    return path