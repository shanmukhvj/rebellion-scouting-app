import multiprocessing

def run_captain():
    import webview
    from master import CaptainAPI, html as captain_html
    api = CaptainAPI()
    webview.create_window("Captain Dashboard", html=captain_html, js_api=api, width=800, height=600)
    webview.start(gui='qt', debug=True)

def run_scouter(num):
    import webview
    from slave import ScoutAPI, html as scout_html
    api = ScoutAPI()
    webview.create_window(f"Scouter {num}", html=scout_html, js_api=api, width=1200, height=700)
    webview.start(gui='qt', debug=True)

if __name__ == "__main__":
    processes = []

    # Launch Captain
    processes.append(multiprocessing.Process(target=run_captain))

    # Launch 3 Scouters
    for i in range(1, 4):
        processes.append(multiprocessing.Process(target=run_scouter, args=(i,)))

    # Start all processes
    for p in processes:
        p.start()

    # Wait for all to finish
    for p in processes:
        p.join()
