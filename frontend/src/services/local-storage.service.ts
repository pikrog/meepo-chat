type LocalStorageKeys = 'access_token' | 'server_address';

export function setInLocalStorage(key: LocalStorageKeys, value: string) {
  localStorage.setItem(key, value);
}

export function getFromLocalStorage(key: LocalStorageKeys) {
  return localStorage.getItem(key);
}