"use client"
import React from "react";
import {
  LucideIcon,
  X,
  Upload as Up,
} from "lucide-react";

type propType = {
  id_upload: string;
  Icon: LucideIcon;
  title: string;
  sub_title: string;
  state: File | null;
  changeStateMethod: React.Dispatch<
    React.SetStateAction<File | null>
  >;
};




function Upload({
  id_upload,
  Icon,
  title,
  sub_title,
  state,
  changeStateMethod,
}: propType) {


  return (

    <div className="flex flex-col w-132.5 h-150">

      <div className="flex gap-2 w-full">

        <div className="h-10 w-10 grid place-items-center rounded-xl bg-violet-400/10">
          <Icon
            size={17}
            className="text-violet-400"
          />
        </div>

        <div>
          <p className="font-semibold text-md">
            {title}
          </p>

          <p className="text-sm text-gray-300/70">
            {sub_title}
          </p>
        </div>

      </div>

      <input
        type="file"
        id={id_upload}
        className="hidden"
        accept="image/*"
        onChange={(e) => {
          const file = e.target.files?.[0];

          if (file) {
            changeStateMethod(file);
          }
        }}
      />

      <div
        
        className="
          rounded-2xl
          border-dashed
          
          border-2
          border-gray-500/50
          bg-slate-900/40
          w-full
          mt-5
          flex-1
          overflow-hidden
          transition-all
          duration-300
          hover:border-violet-400/60
          hover:shadow-2xl
          hover:shadow-violet-300/20
          relative
        "
      >

        {!state ? (
          <label htmlFor={id_upload} className="cursor-pointer
          flex
          flex-col
          items-center
          justify-center h-full w-full ">
            <div className="bg-violet-500/10 h-15 w-15 rounded-full text-violet-400 grid place-items-center">
              <Up size={25} />
            </div>

            <p className="text-sm my-2">
              Drop image or{" "}
              <span className="text-violet-400 font-semibold">
                browse
              </span>
            </p>

            <p className="text-xs text-gray-400">
              PNG, JPG, WEBP up to 10MB
            </p>
          </label>
        ) : (
            <>
           
          <img
            src={URL.createObjectURL(state)}
            alt="preview"
            className="w-full h-full object-cover"
          />
          <button onClick={()=>changeStateMethod(null)} className="absolute h-8 w-8 grid cursor-pointer place-items-center rounded-full bg-black/30 bottom-3 right-3"><X size={15} color="white"/></button>
           </>
        )}

      </div>
    </div>
  );
}

export default Upload;