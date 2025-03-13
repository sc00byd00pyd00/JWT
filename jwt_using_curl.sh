#!/bin/bash

API_URL="http://127.0.0.1:5000"
ACCESS_TOKEN=""
REFRESH_TOKEN=""

login() {
    read -p "Username: " username
    read -s -p "Password: " password
    echo ""
    
    response=$(curl -s -X POST "$API_URL/login" -H "Content-Type: application/json" \
        -d "{\"username\": \"$username\", \"password\": \"$password\"}")
    
    ACCESS_TOKEN=$(echo $response | jq -r '.access_token')
    REFRESH_TOKEN=$(echo $response | jq -r '.refresh_token')
    
    if [ "$ACCESS_TOKEN" != "null" ]; then
        echo "Login successful! Access token obtained."
    else
        echo "Login failed!"
    fi
}

refresh_token() {
    response=$(curl -s -X POST "$API_URL/refresh" -H "Authorization: Bearer $REFRESH_TOKEN")
    ACCESS_TOKEN=$(echo $response | jq -r '.access_token')
    
    if [ "$ACCESS_TOKEN" != "null" ]; then
        echo "Token refreshed successfully!"
    else
        echo "Token refresh failed!"
    fi
}

access_protected() {
    response=$(curl -s -X GET "$API_URL/protected" -H "Authorization: Bearer $ACCESS_TOKEN")
    echo "Response: $response"
}

list_users() {
    response=$(curl -s -X GET "$API_URL/users" -H "Authorization: Bearer $ACCESS_TOKEN")
    echo "Users: $response"
}

add_user() {
    read -p "New username: " new_username
    read -s -p "New password: " new_password
    echo ""
    read -p "Role (admin/user): " role
    
    response=$(curl -s -X POST "$API_URL/add_user" -H "Authorization: Bearer $ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"username\": \"$new_username\", \"password\": \"$new_password\", \"role\": \"$role\"}")
    echo "Response: $response"
}

delete_user() {
    read -p "Username to delete: " del_username
    
    response=$(curl -s -X DELETE "$API_URL/delete_user" -H "Authorization: Bearer $ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"username\": \"$del_username\"}")
    echo "Response: $response"
}

menu() {
    echo "1) Login"
    echo "2) Refresh Token"
    echo "3) Access Protected Route"
    echo "4) List Users"
    echo "5) Add User (Admin Only)"
    echo "6) Delete User (Admin Only)"
    echo "7) Exit"
    read -p "Choose an option: " choice
    
    case $choice in
        1) login ;;
        2) refresh_token ;;
        3) access_protected ;;
        4) list_users ;;
        5) add_user ;;
        6) delete_user ;;
        7) exit 0 ;;
        *) echo "Invalid option" ;;
    esac
}

while true; do
    menu
done
