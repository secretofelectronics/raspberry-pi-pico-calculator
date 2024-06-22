from machine import Pin, I2C
from time import sleep
from i2c_lcd import I2cLcd

# LCD configuration
I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# Keypad configuration
ROWS = [2, 3, 4, 5]
COLS = [6, 7, 8, 9]

keypad = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

row_pins = [Pin(ROWS[i], Pin.OUT) for i in range(4)]
col_pins = [Pin(COLS[i], Pin.IN, Pin.PULL_DOWN) for i in range(4)]

def scan_keypad():
    for row in range(4):
        for r_pin in row_pins:
            r_pin.value(0)
        row_pins[row].value(1)
        for col in range(4):
            if col_pins[col].value() == 1:
                return keypad[row][col]
    return None

def main():
    lcd.clear()
    expression = ""
    lcd.putstr("Calculator Ready")
    sleep(2)
    lcd.clear()

    while True:
        key = scan_keypad()
        if key:
            if key == '#':  # Clear the display and reset expression
                expression = ""
                lcd.clear()
            elif key == '*':  # Calculate result
                try:
                    result = str(eval(expression))
                    lcd.clear()
                    lcd.putstr(result)
                    expression = result
                except:
                    lcd.clear()
                    lcd.putstr("Error")
                    expression = ""
                sleep(2)
                lcd.clear()
                expression = ""  # Clear expression after showing result
            elif key in ['A', 'B', 'C', 'D']:
                if key == 'A':
                    expression += '+'
                    lcd.putstr('+')
                elif key == 'B':
                    expression += '-'
                    lcd.putstr('-')
                elif key == 'C':
                    expression += '*'
                    lcd.putstr('*')
                elif key == 'D':
                    expression += '/'
                    lcd.putstr('/')
            else:
                expression += key
                lcd.putstr(key)
            sleep(0.3)  # Debounce delay

if __name__ == "__main__":
    main()