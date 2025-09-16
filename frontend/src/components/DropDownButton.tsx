interface DropDownButtonProps {
  title: string;
  contents: Array<string | number | {id: string, name: string}>;
  onSelect?: (value: any) => void;
  selectedValue?: string | number | null;
}

export default function DropDownButton({
  title, 
  contents, 
  onSelect, 
  selectedValue
}: DropDownButtonProps) {
  
  const handleSelect = (item: string | number | {id: string, name: string}) => {
    if (!onSelect) return;
    
    if (typeof item === 'object' && 'id' in item) {
      onSelect(item.id);
    } else {
      onSelect(item);
    }
  };

  const getDisplayValue = (item: string | number | {id: string, name: string}): string => {
    if (typeof item === 'object' && 'name' in item) {
      return item.name;
    }
    return String(item);
  };

  const getItemKey = (item: string | number | {id: string, name: string}): string => {
    if (typeof item === 'object' && 'id' in item) {
      return item.id;
    }
    return String(item);
  };

  const isSelected = (item: string | number | {id: string, name: string}): boolean => {
    if (!selectedValue) return false;
    
    if (typeof item === 'object' && 'id' in item) {
      return item.id === selectedValue;
    }
    return String(item) === String(selectedValue);
  };

  const getButtonText = (): string => {
    if (!selectedValue) return `${title} ▾`;
    
    if (contents.length > 0) {
      const selectedItem = contents.find(item => {
        if (typeof item === 'object' && 'id' in item) {
          return item.id === selectedValue;
        }
        return String(item) === String(selectedValue);
      });
      
      if (selectedItem) {
        return `${title}: ${getDisplayValue(selectedItem)}`;
      }
    }
    
    return `${title}: ${selectedValue}`;
  };

  return (
    <>
      <div className="dropdown dropdown-start">
        <div 
          tabIndex={0} 
          role="button" 
          className="responsive
            opacity-85
            rounded-xl
            bg-gradient-to-r from-[#FCCEFD] to-[#F7C1EF]/47
            hover:bg-purple-700
            text-purple-950
            font-black
            text-[1.1em]
            px-12
            py-5
            border-1
            border-white
            font-(family-name: Galano Grotesque Alt)"
        >
          {getButtonText()}
        </div>
        <ul 
          tabIndex={0} 
          className="dropdown-content menu
            bg-gradient-to-r from-[#FCCEFD] to-[#F7C1EF]/85
            backdrop-blur-xs
            text-purple-900
            rounded-box
            z-1 w-52 p-2
            shadow-sm"
        >
          {contents && contents.length > 0 ? contents.map((content) => {
            return (
              <li key={getItemKey(content)}>
                <a 
                  onClick={() => handleSelect(content)}
                  className={isSelected(content) ? 'bg-purple-200' : ''}
                >
                  {getDisplayValue(content)}
                </a>
              </li>
            )
          }) : (
            <li><a>There's no filter</a></li>
          )}
        </ul>
      </div>
    </>
  )
}