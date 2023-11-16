def enrich_format_message(*args,**kwargs):
    return f"""
    Return the text given below with appropriate emojis
    message: {kwargs['message']}

    """