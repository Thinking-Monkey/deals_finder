export default function DropDownButton({title}: {title: string}){
   return (
//       <button  type="button"
//                onClick={() => {}}
//                className="
//                   responsive
//                   opacity-85
//                   rounded-3xl
//                   bg-gradient-to-r from-[#FCCEFD] to-[#F7C1EF]/47
//                   hover:bg-purple-700
//                   text-white
//                   font-black
//                   text-[1.1em]
//                   px-12
//                   py-5
//                   border-1
//                   border-white
//                   font-(family-name: Galano Grotesque Alt)
//                 ">{title}</button>
//   )
      <>
         <div className="dropdown dropdown-end">
         <div tabIndex={0} role="button" className="  responsive
                                                      opacity-85
                                                      rounded-xl
                                                      bg-gradient-to-r from-[#FCCEFD] to-[#F7C1EF]/47
                                                      hover:bg-purple-700
                                                      text-white
                                                      font-black
                                                      text-[1.1em]
                                                      px-12
                                                      py-5
                                                      border-1
                                                      border-white
                                                      font-(family-name: Galano Grotesque Alt)">Select filter ▾</div>
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