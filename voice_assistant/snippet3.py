def find_command(self, request: str) -> Command | None:
    global all_commands
    
    result_command: Command | None = None
    max_weight = float(0)
    
    for command in all_commands:
        
        full_weight = float(0)
        
        for weight, strings in command.keywords.items():
            for keyword in strings:
                match = weight * max(
                    levenshtein.match_partial(request, keyword),                         
                    levenshtein.match_words(request, keyword)
                )
                full_weight += match
        
        if full_weight > max_weight:
            max_weight = full_weight
            result_command = command
    
    if max_weight < 15:
        return None
    
    return result_command