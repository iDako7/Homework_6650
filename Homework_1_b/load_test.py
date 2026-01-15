import requests
import time
import matplotlib.pyplot as plt
import numpy as np


def load_test(url, duration_seconds=30):
    """
    Send continuous GET requests to a URL for a specified duration.
    Returns a list of response times in milliseconds.
    """
    response_times = []
    start_time = time.time()
    end_time = start_time + duration_seconds

    print(f"Starting load test for {duration_seconds} seconds...")
    print(f"Target URL: {url}")
    print("-" * 50)

    request_count = 0
    while time.time() < end_time:
        try:
            # Time the request
            start_request = time.time()
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise exception for 4xx/5xx status codes
            end_request = time.time()

            # Calculate response time in milliseconds
            response_time = (end_request - start_request) * 1000
            response_times.append(response_time)
            request_count += 1

            # Print progress every 10 requests
            if request_count % 10 == 0:
                print(
                    f"Completed {request_count} requests... Latest: {response_time:.2f}ms"
                )

        except requests.exceptions.RequestException as e:
            print(f"Request {request_count + 1} failed: {e}")

    print("-" * 50)
    print(f"Load test complete! Total requests: {len(response_times)}")
    return response_times


def analyze_and_plot(response_times):
    """
    Generate statistics and visualizations for response times.
    """
    if not response_times:
        print("No data to analyze!")
        return

    # Calculate statistics
    stats = {
        "Total Requests": len(response_times),
        "Average (ms)": np.mean(response_times),
        "Median (ms)": np.median(response_times),
        "Std Dev (ms)": np.std(response_times),
        "Min (ms)": min(response_times),
        "Max (ms)": max(response_times),
        "95th Percentile (ms)": np.percentile(response_times, 95),
        "99th Percentile (ms)": np.percentile(response_times, 99),
    }

    # Print statistics
    print("\n" + "=" * 50)
    print("STATISTICS")
    print("=" * 50)
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"{key}: {value:.2f}")
        else:
            print(f"{key}: {value}")

    # Create visualizations
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    # Histogram
    axes[0].hist(
        response_times, bins=50, alpha=0.7, color="steelblue", edgecolor="black"
    )
    axes[0].axvline(
        np.mean(response_times),
        color="red",
        linestyle="--",
        label=f"Mean: {np.mean(response_times):.2f}ms",
    )
    axes[0].axvline(
        np.percentile(response_times, 95),
        color="orange",
        linestyle="--",
        label=f"95th %ile: {np.percentile(response_times, 95):.2f}ms",
    )
    axes[0].set_xlabel("Response Time (ms)")
    axes[0].set_ylabel("Frequency")
    axes[0].set_title("Distribution of Response Times")
    axes[0].legend()

    # Scatter plot over time
    axes[1].scatter(
        range(len(response_times)), response_times, alpha=0.5, s=10, color="steelblue"
    )
    axes[1].axhline(np.mean(response_times), color="red", linestyle="--", label="Mean")
    axes[1].set_xlabel("Request Number")
    axes[1].set_ylabel("Response Time (ms)")
    axes[1].set_title("Response Times Over Time")
    axes[1].legend()

    plt.tight_layout()
    plt.savefig("response_times.png", dpi=150)
    print("\nGraph saved as 'response_times.png'")
    plt.show()


if __name__ == "__main__":
    # ============================================
    # CHANGE THIS TO YOUR EC2 PUBLIC IP ADDRESS!
    # ============================================
    EC2_PUBLIC_IP = "16.148.7.157"  # Updated to your EC2 IP

    URL = f"http://{EC2_PUBLIC_IP}:8080/albums"

    # Run the test
    print("=" * 50)
    print("EC2 LOAD TEST")
    print("=" * 50)

    response_times = load_test(URL, duration_seconds=30)

    if response_times:
        analyze_and_plot(response_times)
