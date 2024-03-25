import Selector from './Selector';

export default async function CompanySelector() {
    await new Promise(resolve => setTimeout(resolve, 1000))
    return (
        <div>
            <div className='relative w-1000 flex'>
                <div className='mb-3 ml-3 text-foreground-white text-base'>
                    {"Select a clearing company"}
                </div>
            </div>
            <div>
                <Selector />
            </div>
        </div>
    )
}