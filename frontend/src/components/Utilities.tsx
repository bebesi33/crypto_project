import { Property } from "csstype";

export const getTextAlign = (dataType: string): Property.TextAlign => {
    let output: string = "right";
    if (dataType === "left") {
      output = "left";
    }
    return output as Property.TextAlign;
  };
