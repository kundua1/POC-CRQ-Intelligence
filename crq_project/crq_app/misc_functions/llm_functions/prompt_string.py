def system_prompt(sop_details):
    prompt = f"""You are an expert in analyzing the project names and then suggesting timelines to users for raising project deployment change requests.
    The goal is to suggest 3 possible timelines in a way so that they do not clash with any other previously scheduled change requests which might have a chance of impact due to the new change request that the user is going to raise."""
    
    # prompt = f"""You are an expert staff who knows how to do repair and maintenance of solar panels.

    # Step 1: Understand whether or not there are objects detected on a solar panel. If yes, then go to step 2.
    # Step 2: Suggest the right course of action to mitigate the risk based on {sop_details}.

    # Strictly follow the below instructions while giving your answer:
    # 1. Please Mention only the steps that should be taken and not anything else.
    # 2. Give step by step instructions and only in plain text format.
    # 3. After mentioning the steps, do not mention anything else.
    # """
    
    return prompt


def user_prompt(project_name, dependent_applications):
    prompt = f"""
    Please suggest 3 different timelines for the following project: {project_name}.
    The project has dependency on the below applications which might be impacted.
    Applications: {dependent_applications}
    """
    
    return prompt