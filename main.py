from pipeline.orchestrator import run_pipeline


if __name__ == "__main__":
    print()
    letterboxd_username = input("Enter Letterboxd username: ")
    print()

    run_pipeline(letterboxd_username)
