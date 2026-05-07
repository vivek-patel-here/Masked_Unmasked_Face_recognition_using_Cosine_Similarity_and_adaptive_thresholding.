"use client"
import React from 'react'
import { Sparkles,CircleAlert ,ShieldCheck , OctagonMinus} from 'lucide-react'
type OutputType = {
        Success : boolean,
        Similarity? : number,
        "Adaptive Threshold"? : number,
        Match? : boolean,
        Message? : string
    }

function Placeholder() {
  return (
      <div className='border-2 bg-slate-900/40 w-180 h-40 mt-5 rounded-xl border-dashed border-gray-500/50 flex justify-center items-center flex-col gap-3'>
        <Sparkles className=' text-gray-300'/>
        <p className='text-md text-gray-300'>Upload both images and click <span className='font-semibold text-white'>Verify Match</span> to see results.</p>
      </div>
  )
}


function Success({output}:{output:OutputType}) {

  const similarity = (output.Similarity ?? 0) * 100;
  const threshold = (output["Adaptive Threshold"] ?? 0.7) * 100;
  return (
    <div className="border border-emerald-500 bg-linear-to-r from-emerald-500/15 to-emerald-200/5 w-180 min-h-40 mt-5 rounded-2xl p-5 flex flex-col gap-5">

      {/* Top Section */}
      <div className="flex items-center gap-4 w-full">

        <div className="h-12 w-12 rounded-full grid place-items-center bg-emerald-400/20 shrink-0">
          <ShieldCheck size={25} className="text-emerald-500" />
        </div>

        <div>
          <p className="font-semibold text-lg text-white">
            Same Person
          </p>

          <p className="text-sm text-gray-400">
            Facial features align across both images.
          </p>
        </div>

      </div>

      {/* Confidence Section */}
      <div className="w-full space-y-2">

        <div className="flex items-center justify-between">
          <p className="text-sm font-medium text-gray-200">
            Similarity Score
          </p>

          <p className="text-sm font-semibold text-emerald-400">
            {similarity.toFixed(1)}%
          </p>
        </div>

        {/* Progress Bar */}
        <div className="h-2 w-full overflow-hidden rounded-full bg-zinc-800">

          <div
            className="h-full rounded-full bg-emerald-500 transition-all duration-500"
            style={{
              width: `${similarity}%`,
            }}
          />

        </div>
         <div>Adaptive Threshold : {threshold.toFixed(1)}%</div>


      </div>
    </div>
  );
}


function Failure({output}:{output:OutputType}) {
  const similarity = (output.Similarity ?? 0) * 100;
  const threshold = (output["Adaptive Threshold"] ?? 0.7) * 100;
  return (
    <div className="border border-red-500 bg-linear-to-r from-red-500/15 to-red-200/5 w-180 min-h-40 mt-5 rounded-2xl p-5 flex flex-col gap-5">

      {/* Top Section */}
      <div className="flex items-center gap-4 w-full">

        <div className="h-12 w-12 rounded-full grid place-items-center bg-red-400/20 shrink-0">
          <CircleAlert size={25} className="text-red-500" />
        </div>

        <div>
          <p className="font-semibold text-lg text-white">
            Different Person
          </p>

          <p className="text-sm text-gray-400">
            Facial features do not match within tolerance.
          </p>
        </div>

      </div>

      {/* Confidence Section */}
      <div className="w-full space-y-2">

        <div className="flex items-center justify-between">
          <p className="text-sm font-medium text-gray-200">
            Similarity Score
          </p>

          <p className="text-sm font-semibold text-red-400">
            {similarity.toFixed(1)}%
          </p>
        </div>

        {/* Progress Bar */}
        <div className="h-2 w-full overflow-hidden rounded-full bg-zinc-800">

          <div
            className="h-full rounded-full bg-red-500 transition-all duration-500"
            style={{
              width: `${similarity}%`,
            }}
          />
        </div>

        <div>Adaptive Threshold : {threshold.toFixed(1)}%</div>
      </div>
    </div>
  );
}


function Error({output}:{output:OutputType}) {
  return (
    <div className="border border-red-500 bg-linear-to-r from-red-500/15 to-red-200/5 w-180 min-h-40 justify-center mt-5 rounded-2xl p-5 flex flex-col gap-5">

      {/* Top Section */}
      <div className="flex items-center gap-4 w-full">

        <div className="h-12 w-12 rounded-full grid place-items-center bg-red-400/20 shrink-0">
          <OctagonMinus size={25} className="text-red-500" />
        </div>

        <div>
          <p className="font-semibold text-lg text-white">
            Error
          </p>

          <p className="text-sm text-gray-400">
            {output.Message ?? "Unable to Process your Request. Please make sure you have used correct Image formate"}
          </p>
        </div>

      </div>
    </div>
  );
}

export {Placeholder , Success , Failure , Error}