'use client';
import { useState } from 'react'
import { useClickAway } from "@uidotdev/usehooks";

type SelectionCallback = (selected: string) => void

export default function DropDownList(
  { className, elements, placeholder, id, selectCallback }:
    { className: string, elements: string[], placeholder: string, id: string, selectCallback?: SelectionCallback }
) {

  if (typeof selectCallback === 'undefined') {
    selectCallback = (selected: string) => { }
  }

  const [isOpen, setIsOpen] = useState(false)
  const [selected, setSelected] = useState('')

  const ref = useClickAway(() => {
    setIsOpen(false)
  });

  return (
    <div className={`${className}`} id={id} ref={ref}>
      <div>
        <button onClick={() => setIsOpen(!isOpen)} className='w-full h-full text-left text-base'>
          <p className='ml-4 mt-3 mb-2'>
            {selected == '' ? placeholder : selected}
          </p>
        </button>
      </div>
      {isOpen &&
        <div className='absolute z-10 border bg-company-grey border-foreground-white rounded-b-2xl rounded-t-2xl origin-top-right w-full mt-2 max-h-64 overflow-auto'>
          <ul>
            {elements.map((element, index) => {
              return (
                <li
                  onClick={() => { setIsOpen(!isOpen); setSelected(element); selectCallback(element); }}
                  className={
                    `flex hover:opacity-50 bg-company-grey ${index == (elements.length - 1) ? "rounded-b-2xl" : ""} ${index == 0 ? "rounded-t-2xl" : ""}`}>
                  <button onClick={() => setIsOpen(!isOpen)} className='w-full h-full text-left text-base'>
                    <p className='ml-4 mt-3 mb-2'>
                      {element}
                    </p>
                  </button>
                </li>
              )
            })}
          </ul>
        </div>
      }
    </div>
  )
}
