export default function DropDownList({ className, elements }: { className: string, elements: any[] }) {
    return (
        <div className={className} onClick={() => { console.log("Div has been clicked") }}>
            
        </div>
    )
}
