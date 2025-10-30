import hashlib
import time
import datetime
import os
import sys
import json

# ==============================================================================
# LUDI Verifier Core Engine - LUDI_VERIFIER.py
# AI 콘텐츠의 불변 진위(Authenticity) 증명을 위한 개념 증명(PoC) 코드
# ProofX / 2025 Draft
# ==============================================================================

def calculate_content_hash(file_path, hash_algorithm='sha256'):
    """
    주어진 파일의 고유한 디지털 지문(해시값)을 계산합니다.
    아주 작은 변화(1바이트 수정)도 새로운 해시로 바뀌므로
    위조/조작 여부를 판별하는 근거로 사용할 수 있습니다.

    :param file_path: 해시값을 계산할 파일 경로
    :param hash_algorithm: 사용할 해시 알고리즘 (기본: sha256)
    :return: 해시값 (hex string) 또는 None (에러 시)
    """
    if not os.path.exists(file_path):
        print(f"[ERROR] 파일을 찾을 수 없습니다: {file_path}")
        return None

    hasher = hashlib.new(hash_algorithm)

    try:
        with open(file_path, 'rb') as f:
            # 64KB씩 읽어서 해시 업데이트 -> 대용량 파일도 처리 가능
            while True:
                chunk = f.read(65536)
                if not chunk:
                    break
                hasher.update(chunk)

        return hasher.hexdigest()

    except Exception as e:
        print(f"[ERROR] 파일 처리 중 오류 발생: {e}")
        return None


def simulate_blockchain_timestamp(content_hash):
    """
    블록체인에 '원본 존재 증명'을 각인하는 과정을 시뮬레이션합니다.
    실제 구현에서는 이 부분이 L2 체인의 스마트 컨트랙트 호출로 치환됩니다.

    :param content_hash: 계산된 콘텐츠 해시
    :return: 블록체인 등록 결과 (dict)
    """

    current_utc = datetime.datetime.utcnow()
    current_unix = int(time.time())

    verification_result = {
        "verifier_name": "LUDI_Verifier_PoC_V1.0",
        "hash_algorithm": "SHA-256",
        "content_hash": content_hash,
        "timestamp_utc": current_utc.isoformat() + "Z",
        "timestamp_unix": current_unix,
        "blockchain_block": "Simulated Block ID: 1A2B3C4D5E",
        "verification_status": "AUTHENTICITY_REGISTERED"
    }

    # 실제 트랜잭션 지연 느낌을 주기 위한 딜레이
    time.sleep(1)

    return verification_result


def run_ludi_verification(file_path):
    """
    1) 파일 해시 계산
    2) 타임스탬프 + 블록체인 각인 시뮬
    3) 결과 출력
    """
    print("==================================================")
    print("🚀 LUDI Verifier: 진위 검증 프로세스 시작")
    print(f"   대상 파일: {file_path}")
    print("==================================================")

    # 1. 해시 계산
    content_hash = calculate_content_hash(file_path)
    if not content_hash:
        print("\n[프로세스 실패] 해시값 계산에 실패했습니다. 파일 경로를 확인하세요.")
        return

    print("\n[1] 콘텐츠 해시값 (Unique Fingerprint) 계산 완료:")
    print(f"    -> {content_hash}")

    # 2. 블록체인 기록 시뮬레이션
    print("\n[2] 블록체인 타임스탬프 기록 중...")
    start_time = time.time()

    verification_data = simulate_blockchain_timestamp(content_hash)

    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)

    print(f"\n[3] 최초 진위 기록 완료 (소요 시간: {elapsed_time}초)")
    print("--------------------------------------------------")
    for key, value in verification_data.items():
        print(f"   * {key.ljust(20)} : {value}")

    print("--------------------------------------------------")
    print("📦 Machine-readable output (API-style):")
    print(json.dumps(verification_data, indent=4, ensure_ascii=False))
    print("--------------------------------------------------")
    print("💡 위 데이터는 '이 시점에 이 파일이 이 상태로 존재했다'는 증거로 사용될 수 있습니다.")
    print("   실제 서비스에서는 이 레코드가 L2 스마트 컨트랙트에 기록됩니다.")


if __name__ == "__main__":
    # 커맨드라인 인자 지원: python3 LUDI_VERIFIER.py myfile.jpg
    if len(sys.argv) > 1:
        TEST_FILE_PATH = sys.argv[1]
    else:
        TEST_FILE_PATH = "sample_content.txt"

        # 샘플 파일이 없으면 자동 생성
        if not os.path.exists(TEST_FILE_PATH):
            try:
                with open(TEST_FILE_PATH, 'w', encoding='utf-8') as f:
                    f.write(
                        "이것은 LUDI Verifier PoC를 위한 샘플 텍스트입니다. "
                        "이 텍스트의 해시값은 블록체인에 영구히 기록된다고 가정합니다."
                    )
                print(f"⭐ 테스트용 파일 '{TEST_FILE_PATH}' 자동 생성됨.")
            except Exception as e:
                print(f"테스트 파일 생성 실패: {e}")
                sys.exit(1)

    run_ludi_verification(TEST_FILE_PATH)
