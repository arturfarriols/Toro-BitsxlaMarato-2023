import React from 'react';


const Header = () => {
    return (
        <div className="py-5">

            <h1 className="mb-4 text-3xl font-extrabold text-gray-900 dark:text-white md:text-5xl lg:text-6xl">
                <span className="text-transparent bg-clip-text bg-gradient-to-r to-emerald-600 from-sky-400">
                Cardiotocography Interpretation
                </span> assisted with AI.
            </h1>
            <p className="text-lg font-normal text-gray-500 lg:text-xl dark:text-gray-400">
                Upload your RCTG files altogether and extract your analysis with a few <i>clicks</i>.
                </p>
        </div>
    );
};

export default Header;