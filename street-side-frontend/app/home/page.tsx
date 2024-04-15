'use client';
import useSWR from 'swr'
import { useState } from 'react';
import { ADRESS } from '@/api/constants'
import { Transition } from '@headlessui/react'

const fetcher = (input: RequestInfo | URL, init?: RequestInit) => fetch(input, init).then(res => res.json())

function setCompanyLinkStyle(isActive: boolean) {
  const activeStyle = "rounded-xl border-solid border-2 border-title-red"
  const inactiveStyle = "hover:font-semibold"
  return `text-xl text-title-red ${isActive ? activeStyle : inactiveStyle}`
}

export default function Home() {
  const { data, error, isLoading } = useSWR(`${ADRESS}/v1/list_companies`, fetcher);

  return (
    <div className='h-full w-4/6'>
      <div className='mb-10 ml-3'>
        <text className='font-bold text-company-grey text-2xl'>
          {`Welcome to the streets!`}
        </text>
      </div>
      <div className='mb-3 ml-3'>
        <text className='font-bold text-company-grey text-foreground-white'>
          {`Why does this app exists ?`}
        </text>
      </div>
      <div>
        <p className="text-foreground-white text-sm indent-8">
          Each clearing center distributes public, quarterly reports on its financial health, which must comply with the reporting rules recommended by the Bank of International Settlements. In practice, the reports are issued at different times, in different formats and are not centralized for quick analysis. This variety of documents increases the time required to analyze them.
        </p>
      </div>
      <div>
        <p className="text-foreground-white text-sm indent-8 mt-3">
          This process can be simply automated.  In addition, clearing reports do not send email or other notifications. There are errors in reports that can be automatically caught. In general, such documents are inconvenient to work with. With the help of automatic collection of data from multiple clearing centers and cross-analysis of their state on the basis of specified risk management parameters - it is possible to improve the quality of risk management and dialog between venues and their clients.
        </p>
      </div>
      <Transition show={(!isLoading && !error)}>
        <div className='m-3'>
          <text className='font-bold text-company-grey text-foreground-white'>
            {`Data is collected from`}
          </text>
        </div>
        <div className="inline-flex">
          {
            (!isLoading && !error) ?
              data.map(
                (company_name) => {
                  return (
                    <div className={`text-base ml-0.5 mr-0.5 text-title-red hover:font-semibold hover:rounded-xl hover:bg-title-red hover:text-background-black`}>
                      <p className={`ml-1 mr-1`}>
                        {company_name}
                      </p>
                    </div>
                  )
              }) : null
          }
        </div>
      </Transition>
    </div>
  );
}
