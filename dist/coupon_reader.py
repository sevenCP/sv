# coupon_reader.py

def read_coupon_codes(filepath):
    coupon_codes = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                coupon_codes.append(line.strip())
    except FileNotFoundError:
        print(f"오류: '{filepath}' 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"파일 읽기 중 오류 발생: {e}")
    return coupon_codes

