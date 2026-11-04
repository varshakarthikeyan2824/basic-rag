
# Local vs Hosted LLM Comparison

## Objective
Compare a small local LLM with a hosted LLM
for extracting information from a company policy.

## Models
- Local: qwen2.5:0.5b using Ollama
- Hosted: openai/gpt-oss-20b using Groq

## Input
Sick Leave Policy containing information about:
- Employee eligibility
- Annual sick leave days
- Reporting procedure

## Results

The local model failed to extract the correct
information. It returned "Not specified" for
sick leave days, provided incorrect eligibility,
and introduced an HR reporting option that was
not present in the policy.

The hosted model correctly extracted all three
details from the same policy.

## Conclusion

The hosted model performed better in this test.
The smaller local model struggled with accurate
information extraction and instruction following.

Possible reasons include model size, training,
and instruction-following capability. This
experiment demonstrates why model selection
and output validation are important in AI applications.
