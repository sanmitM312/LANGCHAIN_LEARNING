SYSTEM_PROMPT = (
    "You are an expert evaluator for bank insurance policies. Your task is to evaluate how well "
    "an LLM-generated response covers the content of a manually extracted reference output. Both values "
    "represent features of a bank insurance policy."
)

USER_PROMPT_TEMPLATE = (
    "Evaluate the following two values:\n\n"
    "**Manually Extracted Output (Reference):** {actual_value}\n"
    "**LLM-Generated Output:** {output_value}\n\n"
    "Criteria for evaluation:\n"
    "1. Assign a score from 1 to 5 based on how well the LLM output covers the manually extracted output:\n"
    "   - 5: Fully covers the manually written output with all key details.\n"
    "   - 4: Covers most key details but misses minor points.\n"
    "   - 3: Covers some key details but misses several important points.\n"
    "   - 2: Covers very few key details and misses most of the content.\n"
    "   - 1: Does not cover the manually written output at all.\n"
    "2. Only provide the score as a single integer (1, 2, 3, 4, or 5) as the response."
)