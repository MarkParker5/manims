Keywords: TypeAlias = dict[float, list[str]] # weight: [keywords...]
  
@dataclass
class Command:
    name: str
    keywords: Keywords
    runner: Callable[[str], str]
      
all_commands: list[Command]
 
   
  
  
  
  
   
  
},   