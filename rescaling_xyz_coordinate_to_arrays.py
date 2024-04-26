import re

def convert_ngc_to_array(file_path):
    array_2d = []
    patterns = {
        'G00': r'G00 X([\d.-]+) Y([\d.-]+) Z([\d.-]+)',
        'G01': r'G01 X([\d.-]+) Y([\d.-]+) Z([\d.-]+)',
        'G02': r'G02 X([\d.-]+) Y([\d.-]+) Z([\d.-]+) I([\d.-]+) J([\d.-]+)',
        'G03': r'G03 X([\d.-]+) Y([\d.-]+) Z([\d.-]+) I([\d.-]+) J([\d.-]+)'
    }

    fallback_pattern = r'(?:G00 Z([\d.-]+))|(?:G00 X([\d.-]+) Y([\d.-]+))'

    with open(file_path, 'r') as file:
        for line in file:
            match = re.findall(fallback_pattern, line)
            if match:
                if match[0][0]:
                    z = float(match[0][0]) + 189.0
                    array_2d.append([0.0, 0.0, z])
                else:
                    x, y = [float(value) * 0.5589997037 for value in match[0][1:3]]
                    y += 200.0
                    array_2d.append([x, y])
            else:
                for gcode, pattern in patterns.items():
                    if line.startswith(gcode):
                        match = re.findall(pattern, line)
                        if match:
                            x, y = [float(value) * 0.5589997037 for value in match[0][:2]]
                            y += 200.0
                            z = float(match[0][2]) + 189.0
                            array_2d.append([x, y, z])
                        break

    return array_2d

# Usage: Replace "path/to/your/file.ngc" with the desired file path
ngc_file_path = "path/to/your/file.ngc"
array = convert_ngc_to_array(ngc_file_path)
print(array)