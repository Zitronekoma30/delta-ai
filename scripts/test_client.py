import requests
import time

def get_next_sentence() -> requests.Response | None:
    try:
        r = requests.get("http://127.0.0.1:5000/next-sentence", timeout=None)
        if r.status_code == 204:
            return None
        r.raise_for_status()
        return r
    except requests.exceptions.ConnectionError:
        print("❌ Connection error when requesting sentence - is the server running?")
        return None
    except requests.exceptions.Timeout:
        print("❌ Timeout when requesting sentence")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP error when requesting sentence: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error when requesting sentence: {e}")
        return None


def send_prompt(prompt: str) -> requests.Response | None:
    t0 = time.time()

    try:
        r = requests.post(
            "http://127.0.0.1:5000/chat-stream",
            json={"input": prompt.strip()}
        )
        r.raise_for_status()
        t1 = time.time()
        print(f"🕒 LLM: {t1 - t0:.2f}s")
        return r
    except requests.exceptions.ConnectionError:
        print("❌ Connection error when sending prompt - is the server running?")
        return None
    except requests.exceptions.Timeout:
        print("❌ Timeout when sending prompt")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP error when sending prompt: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error when sending prompt: {e}")
        return None

def main():
    print("Delta test client started")

    try:
        while True:
            try:
                msg = input("message> ")
                if not msg.strip():
                    continue
                
                response = send_prompt(msg)
                if response is None:
                    print("❌ Failed to send prompt, trying again...")
                    continue
                
                print(f"✅ Response: {response.status_code}")

                sentence = get_next_sentence()
                while sentence is not None:
                    print(f"📝 sentence: {sentence.text if hasattr(sentence, 'text') else sentence.json()}")
                    sentence = get_next_sentence()
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error in main loop: {e}")
                continue
                
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)