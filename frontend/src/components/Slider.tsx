export default function Slider(){
  return (
    <>
    <div className="w-full max-w-xs">
        <input type="range" min={0} max="100" value="25" className="range" step="25" />
        <div className="flex justify-between px-2.5 mt-2 text-xs">
            <span>0</span>
            <span>1</span>
            <span>2</span>
            <span>3</span>
            <span>4</span>
    </div>
    </div>
    </>
  );
}