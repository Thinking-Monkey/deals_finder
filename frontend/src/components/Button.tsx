export default function Button({title, onClick}: {title: string, onClick: () => void}){
   return (
      <button  type="button"
               onClick={onClick}
               className="
                  rounded-[360px]
                  bg-gradient-to-r from-[#FCCEFD] to-[#F7C1EF]/47
                  hover:bg-purple-700
                  text-purple-700
                  font-black
                  text-[1.1em]
                  px-12
                  py-5
                  border-1
                  border-white
                  font-(family-name: Galano Grotesque Alt)
                ">{title}</button>
  )
}