export default function DropDownButton({title}: {title: string}){
   return (
      <>
         <div className="dropdown dropdown-start">
         <div tabIndex={0} role="button" className="  responsive
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
                                                      font-(family-name: Galano Grotesque Alt)">{title} ▾</div>
         <ul tabIndex={0} className="  dropdown-content menu 
                                       bg-gradient-to-r from-[#FCCEFD] to-[#F7C1EF]/85
                                       backdrop-blur-xs
                                       text-purple-900 
                                       rounded-box 
                                       z-1 w-52 p-2 
                                       shadow-sm">
            <li><a>Item 1</a></li>
            <li><a>Item 2</a></li>
         </ul>
         </div>
      </>
   )
}