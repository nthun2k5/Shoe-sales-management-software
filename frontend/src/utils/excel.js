import * as XLSX from 'xlsx';

/**
 * Xuất dữ liệu ra file Excel
 * @param {Array} data - Mảng các object dữ liệu
 * @param {String} fileName - Tên file xuất ra
 * @param {String} sheetName - Tên sheet
 */
export const exportToExcel = (data, fileName = 'export', sheetName = 'Sheet1') => {
  if (!data || data.length === 0) {
    alert('Không có dữ liệu để xuất');
    return;
  }
  
  const worksheet = XLSX.utils.json_to_sheet(data);
  
  // Tự động căn chỉnh độ rộng cột
  const objectMaxLength = [];
  data.forEach(obj => {
    Object.entries(obj).forEach(([key, value], idx) => {
      const columnValue = value !== null && value !== undefined ? String(value) : '';
      const maxLength = Math.max(columnValue.length, key.length);
      if (!objectMaxLength[idx] || objectMaxLength[idx] < maxLength) {
        objectMaxLength[idx] = maxLength;
      }
    });
  });
  worksheet['!cols'] = objectMaxLength.map(w => ({ wch: w + 2 }));

  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, sheetName);
  
  // Tạo tên file với timestamp
  const date = new Date();
  const timestamp = `${date.getFullYear()}${(date.getMonth()+1).toString().padStart(2, '0')}${date.getDate().toString().padStart(2, '0')}_${date.getHours().toString().padStart(2, '0')}${date.getMinutes().toString().padStart(2, '0')}`;
  
  XLSX.writeFile(workbook, `${fileName}_${timestamp}.xlsx`);
};

