    for px, py in [(rect.left, rect.top), (rect.right-1, rect.top),
                        (rect.left, rect.bottom-1), (rect.right-1, rect.bottom-1)]:
                cr, cc = py // CELL, px // CELL
                if not (0 <= cr < rows and 0 <= cc < cols):
                    return False

            # Check walls of every cell near the player (small margin covers wall thickness)
            t = 2  # half of wall thickness (walls are drawn 3px wide; 4px used for collision)
            area = rect.inflate(2*t, 2*t)
            r0 = max(0, area.top // CELL)
            r1 = min(rows - 1, (area.bottom - 1) // CELL)
            c0 = max(0, area.left // CELL)
            c1 = min(cols - 1, (area.right - 1) // CELL)

            for r in range(r0, r1 + 1):
                for c in range(c0, c1 + 1):
                    x, y = c * CELL, r * CELL
                    top, bottom, right, left = walls[r][c]
                    if top and rect.colliderect(pygame.Rect(x - t, y - t, CELL + 2*t, 2*t)):
                        return False
                    if bottom and rect.colliderect(pygame.Rect(x - t, y + CELL - t, CELL + 2*t, 2*t)):
                        return False
                    if right and rect.colliderect(pygame.Rect(x + CELL - t, y - t, 2*t, CELL + 2*t)):
                        return False
                    if left and rect.colliderect(pygame.Rect(x - t, y - t, 2*t, CELL + 2*t)):
                        return False
            return True