def load_resume(path: str) -> str:
	with open(path, "r", encoding="utf-8") as f:
		return f.read()

def main():
	print(load_resume("test_data/resume_test.txt"))

if __name__ == '__main__':
	main()