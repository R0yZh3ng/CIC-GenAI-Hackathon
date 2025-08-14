import React from 'react';
import { Link } from 'react-router-dom';
import Lebron from '../assets/Lebron.png';

function Home() {
	return (
		<div className="h-full w-full m-0 p-0 bg-[#F9F4F1] flex overflow-hidden">
			{/* Left: Lebron image anchored to bottom */}
			<div className="flex-1 h-full overflow-visible flex items-end justify-center">
				<img
					src={Lebron}
					alt="LeBron James"
					className="w-[80%] sm:w-[75%] md:w-[70%] lg:w-[65%] xl:w-[60%] h-auto object-contain object-bottom select-none pointer-events-none translate-y-[1px]"
				/>
			</div>

			{/* Right: Title, subtitle, button */}
			<div className="flex-1 h-full flex flex-col justify-center items-start px-8 sm:px-12 md:px-16 lg:px-20">
				<div className="leading-tight">
					<div className="font-serif font-black text-[clamp(2.5rem,5vw,7rem)] text-[#171717] tracking-tight">LE-</div>
					<div className="font-serif font-black text-[clamp(3rem,6vw,8rem)] text-[#171717] tracking-tight -mt-2">CRUITER.AI</div>
				</div>
        <div className="flex flex-col items-center py-10 sm:py-12  md:py-14 lg:py-16 ">
          <p className="mt-8 sm:mt-10 md:mt-12 text-[clamp(1.125rem,2.5vw,2.25rem)] text-[#1f1f1f] font-medium leading-relaxed">
            Practice behavioral and technical interviews.
          </p>
					<Link to="/behavior">
						<div className="bg-[#2c2c2c] hover:bg-[#444444] rounded-[5px] text-[#ffffff]" style={{padding: '5px 40px', width: '35vw', margin: '20px 0px 20px', marginTop: '20px'}}>
							<p className="text-white text-center text-lg font-medium">Start Interview</p>
						</div>
					</Link>
        </div>
			</div>
		</div>
	);
}

export default Home;
