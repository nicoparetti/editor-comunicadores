import React from 'react';
import {Composition} from 'remotion';
import {cargarFuentes} from './fuentes';
import {Prueba} from './plantillas/Prueba';
import {TableroEstilo} from './plantillas/TableroEstilo';

cargarFuentes();

// Composiciones fijas del motor. Cada video agrega las suyas (montaje dirigido por
// 3_Videos editados/<nombre>/trabajo/timeline.json con el componente Montaje de src/video/Montaje.tsx).
export const Root: React.FC = () => {
  return (
    <>
      <Composition id="TableroEstilo" component={TableroEstilo} durationInFrames={1} fps={30} width={1920} height={1080} defaultProps={{estilo: 'A'}} />
      <Composition id="Prueba" component={Prueba} durationInFrames={60} fps={30} width={1920} height={1080} />
      <Composition id="PruebaVertical" component={Prueba} durationInFrames={60} fps={30} width={1080} height={1920} />
    </>
  );
};
