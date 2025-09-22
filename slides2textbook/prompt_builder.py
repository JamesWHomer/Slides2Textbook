def bullet_prompt_builder(**prompts):
    prompt = ""
    for key, value in prompts.items():
        prompt += f" - {value}\n"
    return prompt

