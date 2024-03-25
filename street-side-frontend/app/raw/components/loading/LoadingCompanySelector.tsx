import Selector from './Selector';

export default function LoadingCompanySelector() {
    return (
        <div className='animate-pulse'>
            <div className='relative flex'>
                <div className='mb-3 ml-3 text-foreground-white text-base'>
                    {"Loading accessible infromation..."}
                </div>
            </div>
            <div>
                <Selector />
            </div>
        </div>
    )
}