import numpy as np
import gradio as gr


def generate_scores(n):
    n = int(n)

    names = np.array([f"Student {i+1}" for i in range(n)])
    scores = np.random.randint(0, 101, size=n)

    table = np.column_stack((names, scores))

    return table, table


def score_statistics(data):
    data = np.array(data)
    scores = data[:, 1].astype(float)

    avg = np.mean(scores)
    highest = np.max(scores)
    lowest = np.min(scores)
    total = np.sum(scores)

    return avg, highest, lowest, total


def pass_fail_analysis(data):
    data = np.array(data)
    scores = data[:, 1].astype(float)

    passed = np.sum(scores >= 40)
    failed = np.sum(scores < 40)

    return passed, failed


def top_students(data):
    data = np.array(data)
    names = data[:, 0]
    scores = data[:, 1].astype(float)

    sorted_idx = np.argsort(scores)[::-1][:3]

    top_names = names[sorted_idx]
    top_scores = scores[sorted_idx]

    return top_names, top_scores


def filter_above(data, threshold):
    data = np.array(data)
    names = data[:, 0]
    scores = data[:, 1].astype(float)
    threshold = float(threshold)

    mask = scores > threshold

    filtered = np.column_stack((names[mask], scores[mask]))

    return filtered


def full_analysis(data):

    if data is None or len(data) == 0:
        return [["Error", "Generate scores first"]]

    avg, highest, lowest, total = score_statistics(data)
    passed, failed = pass_fail_analysis(data)
    top_names, top_scores = top_students(data)

    table = [
        ["Average Score", avg],
        ["Highest Score", highest],
        ["Lowest Score", lowest],
        ["Total Score", total],
        ["Passed Students", passed],
        ["Failed Students", failed],
        ["Top 1", f"{top_names[0]} - {top_scores[0]}"],
        ["Top 2", f"{top_names[1]} - {top_scores[1]}"],
        ["Top 3", f"{top_names[2]} - {top_scores[2]}"],
    ]

    return table


with gr.Blocks(title="Student Score Analyzer") as demo:

    gr.Markdown("# 📊 Student Score Analyzer")

    scores_state = gr.State()

    with gr.Row():
        count_input = gr.Number(value=10, label="Number of Students")
        generate_btn = gr.Button("Generate Scores", variant="primary")

    scores_display = gr.Dataframe(
        headers=["Student", "Score"],
        interactive=False
    )

    generate_btn.click(
        generate_scores,
        inputs=count_input,
        outputs=[scores_state, scores_display]
    )

    gr.Markdown("---")

    with gr.Tab("📈 Full Analysis"):
        analyze_btn = gr.Button("Run Analysis", variant="primary")
        analysis_output = gr.Dataframe(
            headers=["Metric", "Value"],
            interactive=False
        )

        analyze_btn.click(
            full_analysis,
            inputs=scores_state,
            outputs=analysis_output
        )

    with gr.Tab("🔍 Filter High Scores"):
        threshold_input = gr.Number(value=75, label="Threshold")
        filter_btn = gr.Button("Filter Scores", variant="primary")
        filter_output = gr.Dataframe(
            headers=["Student", "Score"],
            interactive=False
        )

        filter_btn.click(
            filter_above,
            inputs=[scores_state, threshold_input],
            outputs=filter_output
        )

demo.launch(theme=gr.themes.Soft())
