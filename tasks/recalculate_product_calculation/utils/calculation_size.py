
def calc_square_meters(product_type: str, w: float, h: float, d: float) -> float:
    w2 = w
    h2 = h
    h3 = h
    if product_type == 'armchair':
        pass
    elif product_type == 'chair':
        pass
    elif product_type == 'table':
        pass
    elif product_type == 'bed':
        return w2 * 0.001 * h2 * 0.001 + (h3 * 0.001 * d * 0.001) * 2 + h3 * 0.001 *  w * 0.001
    elif product_type == 'msp':
        return w * 0.001 * h * 0.001;
    elif product_type == 'sofa':
        pass
        # return this.getSquareMetersSofa(product);
    elif product_type == 'pouf':
        return w * 0.001 * d * 0.001;
    elif product_type == 'melochevka':
        return 0
    elif product_type == 'nightstand':
        return w * 0.001 * d * 0.001
    return 0

#     calcSquareMeters(product) {
#         switch (+product.entityTypeId) {
#             case ID_ARMCHAIR:
#                 // Ш*Г
#                 return this.getNumber(product.commonDimensionsWidth) * 0.001 * this.getNumber(product.commonDimensionsDepth) * 0.001;
#             case ID_CHAIR:
#                 // Ш*Г
#                 return this.getNumber(product.commonDimensionsWidth) * 0.001 * this.getNumber(product.commonDimensionsDepth) * 0.001;
#             case ID_TABLE:
#                 //	Ш*Г (Столешка) + Ш*Г (Опора)
#                 return this.getNumber(product.commonDimensionsWidth) * 0.001 * this.getNumber(product.commonDimensionsDepth) * 0.001
#                     + this.getNumber(product.commonDimensionsWidth_2) * 0.001 * this.getNumber(product.commonDimensionsDepth_2) * 0.001;
#             case ID_BED:
#                 // Ш*В (Изголовья) + ((В (царга) * Г (общия))*2)+(В (царга) * Ш (общая))
#                 return this.getNumber(product.commonDimensionsWidth_2) * 0.001 * this.getNumber(product.commonDimensionsHeight_2) * 0.001
#                     + (this.getNumber(product.commonDimensionsHeight_3) * 0.001 * this.getNumber(product.commonDimensionsDepth) * 0.001) * 2
#                     + this.getNumber(product.commonDimensionsHeight_3) * 0.001 *  this.getNumber(product.commonDimensionsWidth) * 0.001;
#             case ID_MSP:
#                 // Кв.м = Ш*В
#                 // console.log("Кв.м (Ш*В) = ", this.getNumber(product.commonDimensionsWidth), this.getNumber(product.commonDimensionsHeight));
#                 // console.log("Кв.м (Ш*В) = ", product.commonDimensionsWidth, product.commonDimensionsHeight);
#                 return this.getNumber(product.commonDimensionsWidth) * 0.001 * this.getNumber(product.commonDimensionsHeight) * 0.001;
#             case ID_SOFA:
#                 return this.getSquareMetersSofa(product);
#             case ID_POUF:
#                 // Ш*Г
#                 return this.getNumber(product.commonDimensionsWidth) * 0.001 * this.getNumber(product.commonDimensionsDepth) * 0.001;
#             case ID_MELOCHEVKA:
#                 return 0;
#             case ID_NIGHTSTAND:
#                 // Ш*Г
#                 return this.getNumber(product.commonDimensionsWidth) * 0.001 * this.getNumber(product.commonDimensionsDepth) * 0.001;
#         }
#         return 0;
#     }
#
#     calcLinearMeters(product) {
#         switch (+product.entityTypeId) {
#             case ID_ARMCHAIR:
#                 // Ш
#                 return this.getNumber(product.commonDimensionsWidth) * 0.001;
#             case ID_CHAIR:
#                 // Ш
#                 return this.getNumber(product.commonDimensionsWidth) * 0.001;
#             case ID_TABLE:
#                 // Ш
#                 return this.getNumber(product.commonDimensionsWidth) * 0.001;
#             case ID_BED:
#                 return 0;
#             case ID_MSP:
#                 // Пог.м	Не расчитывается
#                 return 0;
#             case ID_SOFA:
#                 return this.getLinearMetersSofa(product);
#             case ID_POUF:
#                 // Ш
#                 return this.getNumber(product.commonDimensionsWidth) * 0.001;
#             case ID_MELOCHEVKA:
#                 return 0;
#             case ID_NIGHTSTAND:
#                 // Ш
#                 return this.getNumber(product.commonDimensionsWidth) * 0.001;
#         }
#         return 0;
#
#     }