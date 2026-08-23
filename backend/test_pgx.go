package main

import (
	"database/sql"
	"fmt"
	"os"

	_ "github.com/jackc/pgx/v5/stdlib"
)

func main() {
	url := "postgresql://postgres.aynrqlxjwpgzxjpwmjtv:Sahil%40062005%40@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres"
	db, err := sql.Open("pgx", url)
	if err != nil {
		fmt.Println("Open error:", err)
		os.Exit(1)
	}
	if err := db.Ping(); err != nil {
		fmt.Println("Ping error:", err)
		os.Exit(1)
	}
	fmt.Println("Success!")
}
